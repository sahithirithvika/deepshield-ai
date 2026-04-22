# 🚀 DeepShield AI - Quick Deployment Guide

## ⚡ Fast Track Deployment (5 Minutes)

### Prerequisites Check
✅ Google Cloud SDK installed
✅ Docker Desktop installed
✅ Project ID: `deepshield-ai`

---

## 🎯 Option 1: One-Command Deployment (Recommended)

Run this single command in your terminal from the project directory:

```bash
./deploy.sh
```

That's it! The script will:
1. Fix permissions automatically
2. Configure your project
3. Enable required APIs
4. Build the Docker image
5. Deploy to Cloud Run
6. Give you the live URL

**Expected Time**: 10-15 minutes

---

## 🎯 Option 2: Manual Step-by-Step

If you prefer to run commands manually:

### Step 1: Fix Permissions (if needed)
```bash
sudo chown -R $(whoami) ~/.config/gcloud
```

### Step 2: Initialize gcloud
```bash
gcloud init
```
- Login with your Google account
- Select project: `deepshield-ai`
- Select region: `asia-south1`

### Step 3: Enable APIs
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

### Step 4: Build & Deploy
```bash
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app

gcloud run deploy deepshield-ai \
  --image gcr.io/deepshield-ai/deepshield-app \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

### Step 5: Get Your URL
```bash
gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)'
```

---

## 📋 What You'll Get

After deployment completes, you'll receive:

```
✅ MVP Link: https://deepshield-ai-[hash]-uc.a.run.app
✅ Working Prototype Link: https://deepshield-ai-[hash]-uc.a.run.app
```

**Both links are the same** - it's your fully functional production deployment!

---

## 🧪 Testing Your Deployment

### 1. Open the URL
Click the URL provided after deployment

### 2. Upload Test Content
- Try uploading a sports image
- Try uploading a video file
- Wait 3-5 seconds for analysis

### 3. Verify Features
- ✅ Analysis results displayed
- ✅ Authenticity scores shown
- ✅ Certificate generated
- ✅ PDF download works

---

## 🔧 Troubleshooting

### Issue: Permission Denied
```bash
sudo chown -R $(whoami) ~/.config
```

### Issue: Project Not Found
```bash
gcloud projects list
gcloud config set project deepshield-ai
```

### Issue: Build Fails
```bash
# Check Docker is running
docker ps

# View build logs
gcloud builds list --limit 5
```

### Issue: Deployment Timeout
```bash
# Increase timeout
gcloud run services update deepshield-ai --timeout 600
```

### Issue: Out of Memory
```bash
# Increase memory
gcloud run services update deepshield-ai --memory 4Gi
```

---

## 📊 View Logs

```bash
# Real-time logs
gcloud run logs tail deepshield-ai

# Last 50 lines
gcloud run logs read deepshield-ai --limit 50
```

---

## 🔄 Update Deployment

After making code changes:

```bash
./deploy.sh
```

Or manually:

```bash
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app
gcloud run deploy deepshield-ai --image gcr.io/deepshield-ai/deepshield-app
```

---

## 🗑️ Delete Deployment

```bash
gcloud run services delete deepshield-ai --region asia-south1
```

---

## 💰 Cost Information

**Google Cloud Free Tier includes:**
- 2 million requests/month
- 360,000 GB-seconds/month
- 180,000 vCPU-seconds/month

**Your configuration:**
- Memory: 2Gi
- CPU: 2 vCPU
- Timeout: 300s
- Auto-scaling: 0-10 instances

**Expected cost:** $0-5/month for typical hackathon usage

---

## 📞 Need Help?

**Common Commands:**
```bash
# Check service status
gcloud run services describe deepshield-ai --region asia-south1

# View metrics
gcloud run services list

# Check project
gcloud config get-value project

# Check region
gcloud config get-value run/region
```

**Still stuck?**
- Check DEPLOYMENT.md for detailed guide
- View logs: `gcloud run logs read deepshield-ai`
- Verify Docker is running: `docker ps`

---

## ✅ Success Checklist

- [ ] gcloud SDK installed
- [ ] Docker Desktop running
- [ ] Permissions fixed
- [ ] APIs enabled
- [ ] Image built successfully
- [ ] Service deployed
- [ ] URL received
- [ ] App tested in browser
- [ ] Certificate generation works
- [ ] URL copied for submission

---

## 🎉 You're Done!

Your DeepShield AI app is now live and ready for your hackathon submission!

**Copy your live URL and submit it as:**
- MVP Link: [Your URL]
- Working Prototype Link: [Same URL]

Good luck with your hackathon! 🚀

