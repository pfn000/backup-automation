# 🔄 GitHub Automated Backup System with SMS Notifications

Complete automated backup solution for all your GitHub repositories to Google Drive with SMS and email notifications.

---

## 📋 Features

✅ **Automatic Repository Backups**
- Backs up all public/private repositories
- Scheduled weekly backups (customizable)
- Backup on repository creation
- Backup on major events (push, release)

✅ **Multiple Backup Locations**
- Google Drive (primary)
- Local compressed archives
- Retention management
- Integrity verification

✅ **Smart Notifications**
- SMS alerts via Twilio (to +1-724-831-3809)
- Email summaries
- GitHub Issues for failures
- Real-time status updates

✅ **Monitoring & Health Checks**
- Weekly backup verification
- Storage usage tracking
- Status badges
- Detailed logging

---

## 🚀 Quick Start

### 1. Create Backup Automation Repository

```bash
# Create a new private repository
gh repo create backup-automation --private --source=. --description "Automated GitHub backup system"

# Or create manually on github.com/new
# Name: backup-automation
# Private: Yes
# Description: "Automated backup system for all repositories"
```

### 2. Configure Secrets in GitHub

Go to: `https://github.com/pfn000/backup-automation/settings/secrets/actions`

Add these secrets:

#### **GitHub Token**
```
Secret Name: GITHUB_TOKEN
Value: (Already available in workflow, but you can add a Personal Access Token)
```

#### **Google Drive Configuration (via rclone)**
```
Secret Name: RCLONE_CONFIG
Value: (Base64 encoded rclone config - see setup below)
```

#### **Twilio SMS Setup**
```
Secret Name: TWILIO_ACCOUNT_SID
Value: Your Twilio Account SID

Secret Name: TWILIO_AUTH_TOKEN
Value: Your Twilio Auth Token

Secret Name: TWILIO_PHONE_FROM
Value: Your Twilio phone number (e.g., +1234567890)
```

#### **Email Setup (Optional)**
```
Secret Name: SENDER_EMAIL
Value: Your email address

Secret Name: SENDER_PASSWORD
Value: Your app-specific password (NOT your regular password)

Secret Name: SMTP_SERVER
Value: smtp.gmail.com (for Gmail)

Secret Name: SMTP_PORT
Value: 587
```

---

## 🔧 Setup Instructions

### Step 1: Install GitHub CLI

```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

### Step 2: Authenticate GitHub CLI

```bash
gh auth login
# Follow prompts to authenticate
# Choose HTTPS
# Authorize with browser when prompted
```

### Step 3: Set up Google Drive Backup

#### Option A: Using rclone (Recommended)

```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure Google Drive
rclone config

# Follow prompts:
# 1. Type 'n' for new remote
# 2. Name it 'gdrive'
# 3. Choose 'drive' (Google Drive)
# 4. Authorize with Google account
# 5. No service account needed
# 6. No advanced config needed

# Verify configuration
rclone lsf gdrive:

# Convert to base64 for GitHub secret
cat ~/.config/rclone/rclone.conf | base64 -w 0 > rclone_config.b64
cat rclone_config.b64
# Copy this value to RCLONE_CONFIG secret
```

#### Option B: Using Google Drive Desktop

```bash
# Sync a folder to Google Drive
# Then use standard file upload
```

### Step 4: Set up Twilio SMS Notifications

1. **Create Twilio Account**
   - Go to https://www.twilio.com/try-twilio
   - Sign up with email
   - Verify your email

2. **Get Phone Number**
   - In Twilio Console: Phone Numbers → Buy a number
   - Choose number (US-based recommended)
   - The cost is ~$1/month

3. **Get Credentials**
   - Go to Account → API keys & tokens
   - Copy Account SID
   - Copy Auth Token
   - Copy your Twilio phone number

4. **Test SMS**
   ```bash
   python3 << 'EOF'
   from twilio.rest import Client
   import os
   
   account_sid = "your_account_sid"
   auth_token = "your_auth_token"
   client = Client(account_sid, auth_token)
   
   message = client.messages.create(
       body="Test message from GitHub backup system ✅",
       from_="+1234567890",  # Your Twilio number
       to="+17248313809"      # Your phone
   )
   print(f"Message sent: {message.sid}")
   EOF
   ```

### Step 5: Set up Email Notifications

#### For Gmail:

1. **Enable 2-Factor Authentication**
   - Google Account → Security → 2-Step Verification

2. **Create App Password**
   - Google Account → Security → App passwords
   - Select Mail → Windows Computer (or your device)
   - Google generates 16-character password
   - Use this as SENDER_PASSWORD secret

3. **Test Email**
   ```bash
   python3 << 'EOF'
   import smtplib
   from email.mime.text import MIMEText
   
   sender_email = "your_email@gmail.com"
   sender_password = "your_app_password"
   
   message = MIMEText("Test email from backup system")
   message['Subject'] = "Backup System Test"
   message['From'] = sender_email
   message['To'] = "your_email@gmail.com"
   
   with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
       server.login(sender_email, sender_password)
       server.send_message(message)
   print("✅ Email sent successfully")
   EOF
   ```

### Step 6: Deploy Workflow

1. **Copy workflow file to GitHub**
   ```bash
   mkdir -p .github/workflows
   cp .github-workflows-backup.yml .github/workflows/auto-backup.yml
   git add .github/workflows/auto-backup.yml
   git commit -m "Add automated backup workflow"
   git push
   ```

2. **Copy configuration**
   ```bash
   cp .github-backup-config.json .
   git add .github-backup-config.json
   git commit -m "Add backup configuration"
   git push
   ```

3. **Copy backup script**
   ```bash
   cp backup_manager.py .
   git add backup_manager.py
   git commit -m "Add backup manager script"
   git push
   ```

---

## 📱 SMS Notification Examples

When a backup completes, you'll receive SMS like:

```
✅ Repo PleX backed up to Drive! Status: success @ 03:45

✅ Repo Portfolio- backed up to Drive! Status: success @ 03:52

📦 Weekly GitHub backup SUCCESS at 04:15 - All repos backed to Drive ✅
```

On failure:

```
❌ Repo ClaudePleX backup FAILED - Clone timeout
Check: https://github.com/pfn000/backup-automation/actions
```

---

## 🎛️ Configuration Options

Edit `.github-backup-config.json`:

### Backup Schedule
```json
{
  "backup_config": {
    "backup_schedule": "on-create-and-weekly"
    // Options: "on-create-only", "weekly", "daily", "on-push"
  }
}
```

### Exclude Repositories
```json
{
  "repositories": {
    "exclude_repos": [
      "test-repo",
      "sandbox",
      "archived-project"
    ]
  }
}
```

### Notification Methods
```json
{
  "notifications": {
    "sms": { "enabled": true },
    "email": { "enabled": true },
    "github_issue": { "enabled": true }
  }
}
```

### Custom SMS Template
```json
{
  "notifications": {
    "sms": {
      "message_template": "✅ {repo_name} backed up at {timestamp}"
    }
  }
}
```

---

## 🧪 Manual Testing

### Test the backup script locally:

```bash
# Install dependencies
pip install twilio google-auth-oauthlib google-api-python-client

# Test backup of specific repo
python backup_manager.py PleX

# Test all repos
python backup_manager.py
```

### Test SMS notification:

```bash
python3 << 'EOF'
import os
import json
from backup_manager import GitHubBackupManager

manager = GitHubBackupManager()
manager.send_sms_notification("TestRepo", "success", "This is a test notification")
EOF
```

### Run workflow manually:

```bash
# Trigger the workflow via GitHub CLI
gh workflow run auto-backup.yml --repo pfn000/backup-automation
```

---

## 📊 Monitoring & Status

### Check backup status:

```bash
# View workflow runs
gh run list --repo pfn000/backup-automation

# View latest run details
gh run list --repo pfn000/backup-automation -L 1

# Download backup logs
gh run download <run-id> --repo pfn000/backup-automation
```

### Verify Google Drive backups:

```bash
rclone lsf gdrive:"GitHub Backups"
rclone ls gdrive:"GitHub Backups"
```

### Check backup log file:

```bash
tail -f backup.log
```

---

## 🔐 Security Best Practices

1. **Use Private Repository**
   - backup-automation repo should be private
   - Only you have access to secrets

2. **Rotate Credentials Regularly**
   ```bash
   # Regenerate GitHub token
   # Regenerate Google Drive auth
   # Rotate Twilio credentials
   ```

3. **Use Separate Service Accounts**
   - Don't use personal credentials
   - Create service account for backups

4. **Encrypt Sensitive Files**
   ```bash
   git-crypt lock
   ```

5. **Audit Access**
   - Check GitHub Actions logs regularly
   - Monitor Twilio message logs
   - Track Google Drive access

---

## 🐛 Troubleshooting

### SMS Not Sending
```bash
# Check Twilio credentials
echo $TWILIO_ACCOUNT_SID
echo $TWILIO_AUTH_TOKEN

# Test Twilio connection
python3 -c "from twilio.rest import Client; print('✅ Twilio installed')"

# Check phone number format
# Must be: +1 followed by 10 digits
```

### Google Drive Upload Failing
```bash
# Test rclone
rclone lsf gdrive:

# Reconfigure
rclone config

# Check auth
rclone about gdrive:
```

### Email Not Sending
```bash
# For Gmail: Verify app password (not regular password)
# Check SMTP settings
python3 -c "import smtplib; print('✅ SMTP available')"

# Test connection
telnet smtp.gmail.com 587
```

### Backup Job Taking Too Long
```json
{
  "repositories": {
    "max_size_mb": 1000,
    "timeout_minutes": 60
  }
}
```

---

## 📈 Performance Optimization

### Compress backups to save space:

```json
{
  "google_drive": {
    "compression": "tar.gz",
    "exclude_patterns": [
      "node_modules/",
      ".env",
      "*.lock",
      "dist/",
      ".vscode/"
    ]
  }
}
```

### Run backups during off-peak hours:

```yaml
schedule:
  - cron: '0 2 * * 0'  # 2 AM Sunday (UTC)
```

### Limit number of parallel backups:

```bash
# Modify workflow
max-parallel: 3
```

---

## 📝 Maintenance

### Weekly Checklist
- [ ] Check backup notifications received
- [ ] Verify Google Drive has new backups
- [ ] Review workflow run logs
- [ ] Check storage usage

### Monthly Checklist
- [ ] Verify all repositories backed up
- [ ] Test restore process on a sample repo
- [ ] Update dependencies
- [ ] Review and rotate credentials

### Quarterly Checklist
- [ ] Full restore test
- [ ] Update configuration
- [ ] Review costs (Twilio, storage)
- [ ] Audit access logs

---

## 📞 Support & Troubleshooting

**GitHub Actions Docs:**
https://docs.github.com/en/actions

**Twilio Python Docs:**
https://www.twilio.com/docs/libraries/python

**rclone Documentation:**
https://rclone.org/docs/

**Google Drive API:**
https://developers.google.com/drive/api

---

## 📦 Complete Repository Structure

```
pfn000/backup-automation/
├── .github/
│   └── workflows/
│       └── auto-backup.yml          # Main workflow
├── .github-backup-config.json       # Configuration
├── backup_manager.py                # Backup script
├── README.md                         # This file
├── requirements.txt                 # Python dependencies
├── backups/                         # Local backup directory
│   └── 2026-03-24/
│       ├── PleX.tar.gz
│       ├── ncomsignin.tar.gz
│       └── backup_report.json
└── logs/
    └── backup.log                   # Backup logs
```

---

## ✅ Setup Checklist

- [ ] Created backup-automation repository
- [ ] Added GITHUB_TOKEN secret
- [ ] Set up Google Drive & RCLONE_CONFIG
- [ ] Created Twilio account
- [ ] Added Twilio secrets (SID, Token, Phone)
- [ ] Set up email (optional)
- [ ] Deployed workflow file
- [ ] Copied configuration file
- [ ] Copied backup script
- [ ] Tested SMS notification
- [ ] Tested backup script locally
- [ ] Ran workflow manually to verify
- [ ] Received first SMS notification
- [ ] Verified backup in Google Drive

---

## 🎉 You're All Set!

Your GitHub repositories will now be automatically backed up to Google Drive with SMS notifications!

**Next backups scheduled:**
- Weekly: Every Sunday at 2:00 AM UTC
- On demand: Run manually via `gh workflow run`

**Monitoring:**
- Check notifications on your phone
- View backups in Google Drive > GitHub Backups folder
- Review workflow logs at: https://github.com/pfn000/backup-automation/actions

---

**Created by:** pfn000 (Saidie)  
**Last Updated:** March 24, 2026  
**Status:** ✅ Active & Monitoring
