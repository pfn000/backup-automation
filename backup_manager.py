#!/usr/bin/env python3
"""
GitHub Repository Automatic Backup System with SMS Notifications
Author: pfn000 (Saidie)
Description: Automatically backs up GitHub repositories to Google Drive and sends SMS notifications
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import hashlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GitHubBackupManager:
    """Manages GitHub repository backups to Google Drive with notifications"""
    
    def __init__(self, config_path='.github-backup-config.json'):
        """Initialize backup manager with configuration"""
        self.config_path = config_path
        self.config = self.load_config()
        self.backup_dir = Path(f"backups/{datetime.now().strftime('%Y-%m-%d')}")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from = os.getenv('TWILIO_PHONE_FROM')
        
    def load_config(self):
        """Load backup configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            sys.exit(1)
    
    def get_github_repos(self):
        """Fetch all repositories for authenticated user"""
        logger.info("Fetching GitHub repositories...")
        try:
            cmd = [
                'gh', 'repo', 'list', '--limit', '100',
                '--json', 'name,owner,url,createdAt,updatedAt,size'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Failed to fetch repos: {result.stderr}")
                return []
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            return []
    
    def clone_repository(self, repo_url, repo_name):
        """Clone a repository locally"""
        try:
            clone_path = self.backup_dir / repo_name
            logger.info(f"Cloning {repo_name}...")
            
            cmd = ['git', 'clone', '--mirror', repo_url, str(clone_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"Failed to clone {repo_name}: {result.stderr}")
                return None
            
            logger.info(f"Successfully cloned {repo_name}")
            return clone_path
        except subprocess.TimeoutExpired:
            logger.error(f"Clone timeout for {repo_name}")
            return None
        except Exception as e:
            logger.error(f"Error cloning {repo_name}: {e}")
            return None
    
    def compress_backup(self, backup_path):
        """Compress backup into tar.gz"""
        try:
            archive_path = f"{backup_path}.tar.gz"
            logger.info(f"Compressing {backup_path}...")
            
            cmd = ['tar', '-czf', archive_path, '-C', str(backup_path.parent), backup_path.name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                logger.error(f"Failed to compress: {result.stderr}")
                return None
            
            return archive_path
        except Exception as e:
            logger.error(f"Compression error: {e}")
            return None
    
    def upload_to_drive(self, archive_path):
        """Upload compressed backup to Google Drive"""
        try:
            logger.info(f"Uploading {archive_path} to Google Drive...")
            
            # Using Google Drive CLI (rclone or gdrive command)
            cmd = [
                'rclone', 'copy', archive_path,
                'gdrive:GitHub Backups/',
                '--create-empty-src-dirs'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                logger.warning(f"Google Drive upload may have failed: {result.stderr}")
                logger.info("Note: Configure rclone with: rclone config")
                return False
            
            logger.info(f"Successfully uploaded to Google Drive")
            return True
        except FileNotFoundError:
            logger.warning("rclone not installed. Install with: pip install rclone")
            return False
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False
    
    def send_sms_notification(self, repo_name, status, message=""):
        """Send SMS notification via Twilio"""
        if not self.config['notifications']['sms']['enabled']:
            logger.info("SMS notifications disabled")
            return False
        
        try:
            from twilio.rest import Client
            
            if not all([self.twilio_sid, self.twilio_token, self.twilio_from]):
                logger.warning("Twilio credentials not configured. Skipping SMS.")
                logger.info("Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_FROM env vars")
                return False
            
            client = Client(self.twilio_sid, self.twilio_token)
            phone = self.config['notifications']['sms']['phone_number']
            
            # Format message
            sms_template = self.config['notifications']['sms']['message_template']
            sms_message = sms_template.format(
                repo_name=repo_name,
                status=status,
                timestamp=datetime.now().strftime('%H:%M')
            )
            
            message = client.messages.create(
                body=sms_message,
                from_=self.twilio_from,
                to=phone
            )
            
            logger.info(f"SMS sent successfully: {message.sid}")
            return True
        except ImportError:
            logger.warning("Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"SMS sending failed: {e}")
            return False
    
    def send_email_notification(self, repo_name, status):
        """Send email notification"""
        if not self.config['notifications']['email']['enabled']:
            return True
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            sender_email = os.getenv('SENDER_EMAIL')
            sender_password = os.getenv('SENDER_PASSWORD')
            
            if not all([sender_email, sender_password]):
                logger.warning("Email credentials not configured")
                return False
            
            recipients = self.config['notifications']['email']['recipients']
            
            subject = f"✅ GitHub Backup: {repo_name} - {status.upper()}"
            body = f"""
Repository: {repo_name}
Status: {status}
Timestamp: {datetime.now().isoformat()}
Backup Location: Google Drive/GitHub Backups
            """
            
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = ', '.join(recipients)
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent to {', '.join(recipients)}")
            return True
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return False
    
    def backup_repository(self, repo_name, repo_url):
        """Complete backup workflow for a single repository"""
        logger.info(f"Starting backup for {repo_name}...")
        
        try:
            # Clone
            backup_path = self.clone_repository(repo_url, repo_name)
            if not backup_path:
                self.send_sms_notification(repo_name, "failed", "Clone failed")
                return False
            
            # Compress
            archive = self.compress_backup(backup_path)
            if not archive:
                self.send_sms_notification(repo_name, "failed", "Compression failed")
                return False
            
            # Upload
            uploaded = self.upload_to_drive(archive)
            
            # Notify
            status = "success" if uploaded else "partial"
            self.send_sms_notification(repo_name, status)
            self.send_email_notification(repo_name, status)
            
            logger.info(f"Backup for {repo_name} completed with status: {status}")
            return uploaded
        except Exception as e:
            logger.error(f"Backup failed for {repo_name}: {e}")
            self.send_sms_notification(repo_name, "failed", str(e))
            return False
    
    def backup_all_repositories(self):
        """Backup all user repositories"""
        repos = self.get_github_repos()
        
        if not repos:
            logger.warning("No repositories found")
            return False
        
        logger.info(f"Found {len(repos)} repositories")
        
        successful = 0
        failed = 0
        
        for repo in repos:
            repo_name = repo['name']
            repo_url = repo['url']
            
            if self.should_backup(repo):
                if self.backup_repository(repo_name, repo_url):
                    successful += 1
                else:
                    failed += 1
        
        logger.info(f"Backup summary: {successful} successful, {failed} failed")
        return failed == 0
    
    def should_backup(self, repo):
        """Determine if repository should be backed up"""
        config = self.config['repositories']
        
        # Check exclusions
        if repo['name'] in config['exclude_repos']:
            return False
        
        return True
    
    def create_backup_report(self):
        """Create a backup report/status badge"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'backup_location': 'Google Drive',
            'folder': 'GitHub Backups',
            'total_repos': len(self.get_github_repos())
        }
        
        report_path = self.backup_dir / 'backup_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Backup report created: {report_path}")
        return report


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("GitHub Backup Automation Started")
    logger.info("=" * 60)
    
    try:
        manager = GitHubBackupManager()
        
        # Check if specific repo is provided as argument
        if len(sys.argv) > 1:
            repo_name = sys.argv[1]
            repos = manager.get_github_repos()
            repo = next((r for r in repos if r['name'] == repo_name), None)
            
            if repo:
                manager.backup_repository(repo['name'], repo['url'])
            else:
                logger.error(f"Repository not found: {repo_name}")
        else:
            # Backup all repositories
            manager.backup_all_repositories()
        
        # Create report
        manager.create_backup_report()
        
        logger.info("=" * 60)
        logger.info("GitHub Backup Automation Completed")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
