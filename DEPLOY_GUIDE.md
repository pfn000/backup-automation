# 🚀 BACKUP CORE Repository - Deployment Guide

**Deploy your AI-powered backup dashboard to GitHub with live SMS notifications**

---

## 📋 What You're Deploying

Complete repository containing:
- ✅ **CORE.html** - Live dashboard interface
- ✅ **api-server.js** - Node.js backend with Claude AI integration
- ✅ **package.json** - Dependencies
- ✅ **README.md** - Documentation
- ✅ **.env.example** - Configuration template
- ✅ **.gitignore** - Git configuration

---

## 🎯 Quick Deploy (5 minutes)

### Step 1: Create Repository on GitHub

```bash
# Option A: Using GitHub CLI (recommended)
gh repo create backup-core \
  --private \
  --description "AI-Powered GitHub Backup Dashboard with Live SMS Notifications" \
  --confirm

# Option B: Via GitHub Web
# 1. Go to https://github.com/new
# 2. Repository name: backup-core
# 3. Description: "AI-Powered GitHub Backup Dashboard"
# 4. Private: YES (important!)
# 5. Initialize with README: NO
# 6. Click "Create repository"
```

### Step 2: Clone & Add Files

```bash
# Clone the repository
git clone https://github.com/pfn000/backup-core.git
cd backup-core

# Add all files from outputs/
cp ../CORE.html .
cp ../api-server.js .
cp ../package.json .
cp ../README.md .
cp ../env.example .env.example
cp ../gitignore .gitignore

# Configure git
git config user.email "saidie000@gmail.com"
git config user.name "Saidie"

# Commit and push
git add .
git commit -m "Initial commit: Add BACKUP CORE dashboard with Claude AI integration"
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

```bash
# Check repository
open https://github.com/pfn000/backup-core

# You should see:
# ✅ CORE.html
# ✅ api-server.js
# ✅ package.json
# ✅ README.md
# ✅ .env.example
# ✅ .gitignore
```

---

## 🖥️ Local Setup & Testing

### Step 1: Install Dependencies

```bash
cd backup-core
npm install
```

### Step 2: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your credentials
nano .env
# Or use your editor of choice
```

### Step 3: Add Your Credentials

In `.env`, fill in:
```
CLAUDE_API_KEY=sk-ant-v1-xxxxxxxxxxxxxxxx
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
TWILIO_PHONE_FROM=+1234567890
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
USER_PHONE=+17248313809
```

### Step 4: Start API Server

```bash
npm start
# Server runs on http://localhost:3000
```

### Step 5: Open Dashboard

```bash
# In your browser
open http://localhost:3000/CORE.html

# Or use Python server
python3 -m http.server 8000
open http://localhost:8000/CORE.html
```

---

## 🌐 Deploy to Production

### Option 1: Deploy to Heroku (Free Tier)

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create backup-core-pfn000

# Set environment variables
heroku config:set CLAUDE_API_KEY=sk-ant-v1-xxxxx
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxx
heroku config:set TWILIO_PHONE_FROM=+1234567890
heroku config:set USER_PHONE=+17248313809
heroku config:set GITHUB_TOKEN=ghp_xxxxx

# Deploy
git push heroku main

# View live
heroku open
# Dashboard at: https://backup-core-pfn000.herokuapp.com/CORE.html
```

### Option 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# Dashboard at: https://backup-core-xxx.vercel.app/CORE.html
```

### Option 3: Deploy to AWS Lambda

```bash
# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
serverless config credentials --provider aws

# Deploy
serverless deploy
```

### Option 4: Self-hosted (VPS/Server)

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/pfn000/backup-core.git
cd backup-core

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install dependencies
npm install

# Create .env file
cp .env.example .env
nano .env  # Add your credentials

# Install PM2 for process management
npm install -g pm2

# Start server
pm2 start api-server.js --name "backup-core"
pm2 save
pm2 startup

# Set up reverse proxy (nginx)
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/backup-core
# Add configuration pointing to localhost:3000
sudo ln -s /etc/nginx/sites-available/backup-core /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Access at: https://your-domain.com/CORE.html
```

---

## 🔐 Production Checklist

- [ ] Create repository on GitHub (private)
- [ ] Add `.env` file with credentials (never commit)
- [ ] Test locally with `npm start`
- [ ] Set up deployment (Heroku/Vercel/AWS/VPS)
- [ ] Configure production environment variables
- [ ] Set up custom domain
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure backups in GitHub Actions
- [ ] Test SMS notifications
- [ ] Set up error logging
- [ ] Configure monitoring
- [ ] Set up incident alerts

---

## 🤖 Claude AI Integration

### Connect Claude API

```javascript
// In api-server.js, Claude is auto-initialized:
const config = {
    claudeApiKey: process.env.CLAUDE_API_KEY,
    claudeApiUrl: 'https://api.anthropic.com/v1/messages'
};

// API automatically used by:
// - generateBackupReport()
// - generateSMSMessage()
// - POST /api/backup
```

### Get Claude API Key

1. Go to https://console.anthropic.com
2. Click "API Keys" 
3. Create new key
4. Copy to `.env` as `CLAUDE_API_KEY`

---

## 📱 Twilio SMS Setup

### Get Twilio Credentials

```bash
# 1. Sign up at https://www.twilio.com
# 2. Get Account SID from Console
# 3. Get Auth Token from Console
# 4. Buy a phone number (~$1/month)

# Add to .env:
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
TWILIO_PHONE_FROM=+1XXXXXXXXXX
USER_PHONE=+17248313809
```

### Test SMS

```bash
# Start server
npm start

# In another terminal, test SMS
curl -X POST http://localhost:3000/api/send-sms \
  -H "Content-Type: application/json" \
  -d '{"repoName": "PleX", "customMessage": "Test SMS ✅"}'
```

---

## 🔄 GitHub Integration

### Set Up Webhooks

In your GitHub repo settings:
1. Go to Settings → Webhooks
2. Click "Add webhook"
3. Payload URL: `https://your-domain.com/api/webhook/backup-complete`
4. Content type: `application/json`
5. Trigger on: `Repository events`
6. Active: ✅

---

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:3000/api/health

# Get status
curl http://localhost:3000/api/status

# List repos
curl http://localhost:3000/api/repos

# Trigger backup
curl -X POST http://localhost:3000/api/backup \
  -H "Content-Type: application/json" \
  -d '{"type": "all", "repos": ["PleX", "ncomsignin"]}'

# Send SMS
curl -X POST http://localhost:3000/api/send-sms \
  -H "Content-Type: application/json" \
  -d '{"repoName": "PleX"}'
```

### Test Dashboard

```bash
# Open in browser
open http://localhost:3000/CORE.html

# Try:
# 1. Click "START BACKUP NOW"
# 2. Select repository and click "SEND SMS"
# 3. Watch activity feed
# 4. Check phone for SMS
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Development
npm start  # Logs in console

# Production (PM2)
pm2 logs backup-core

# Heroku
heroku logs --tail

# Docker
docker logs backup-core
```

### Monitor API

```bash
# Health status
curl http://localhost:3000/api/health

# System status
curl http://localhost:3000/api/status
```

---

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
PORT=3001 npm start
```

### Claude API Error

```bash
# Check API key
echo $CLAUDE_API_KEY

# Test API connection
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'
```

### Twilio SMS Not Sending

```bash
# Check credentials
echo $TWILIO_ACCOUNT_SID
echo $TWILIO_AUTH_TOKEN
echo $TWILIO_PHONE_FROM

# Test with Twilio CLI
twilio api:core:messages:create \
  --from=$TWILIO_PHONE_FROM \
  --to=+17248313809 \
  --body="Test message"
```

### Dashboard Not Loading

```bash
# Check if server is running
curl http://localhost:3000/api/health

# Check firewall
sudo ufw allow 3000

# Check CORS settings
# Already configured in api-server.js: cors()
```

---

## 📚 Next Steps

After deployment:

1. **Monitor** - Check logs regularly
2. **Test** - Run weekly test backups
3. **Update** - Keep dependencies current
4. **Secure** - Rotate API keys quarterly
5. **Scale** - Add more repos as needed
6. **Improve** - Gather feedback and iterate

---

## 🎉 Success Indicators

You'll know it's working when:

✅ Dashboard loads at `https://your-domain.com/CORE.html`
✅ API health check returns `{"status":"ok"}`
✅ SMS sends to `+17248313809` on backup trigger
✅ Activity feed updates in real-time
✅ Backups run on schedule
✅ All 10 repos shown as "backed"

---

## 🔗 Useful Links

- **GitHub Repo:** https://github.com/pfn000/backup-core
- **Claude API Docs:** https://docs.anthropic.com
- **Twilio Docs:** https://www.twilio.com/docs
- **Heroku Docs:** https://devcenter.heroku.com
- **Vercel Docs:** https://vercel.com/docs

---

## 📞 Support

**Issues?**
1. Check the troubleshooting section above
2. Review API logs
3. Test each component separately
4. Check GitHub issues

**Questions?**
- Review README.md
- Check api-server.js comments
- Read Claude/Twilio docs

---

## ✅ Deployment Status

- ✅ Repository ready
- ✅ Files committed locally
- ✅ Ready to push to GitHub
- ✅ API server configured
- ✅ Dashboard created
- ✅ Documentation complete

**Next:** Push to GitHub and deploy! 🚀

---

**Created:** March 24, 2026  
**For:** pfn000 (Saidie)  
**Status:** ✅ Production Ready

Your BACKUP CORE dashboard is ready to go live! 🎉
