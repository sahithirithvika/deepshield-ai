# 🚀 DeepShield AI - Command Reference

## Quick Commands

### 🎯 Deploy Everything (One Command)
```bash
./deploy.sh
```

### 🔧 Fix Permissions First
```bash
sudo chown -R $(whoami) ~/.config/gcloud
```

### 📋 Manual Deployment Steps

#### 1. Initialize gcloud
```bash
gcloud init
```
Select:
- Login with your Google account
- Project: `deepshield-ai`
- Region: `asia-south1`

#### 2. Configure Project
```bash
gcloud config set project deepshield-ai
gcloud config set run/region asia-south1
```

#### 3. Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### 4. Build Image
```bash
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app
```

#### 5. Deploy to Cloud Run
```bash
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

#### 6. Get Live URL
```bash
gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)'
```

---

## 📊 Monitoring Commands

### View Service Status
```bash
gcloud run services describe deepshield-ai --region asia-south1
```

### View Logs (Real-time)
```bash
gcloud run logs tail deepshield-ai
```

### View Logs (Last 50 lines)
```bash
gcloud run logs read deepshield-ai --limit 50
```

### List All Services
```bash
gcloud run services list
```

### View Metrics
```bash
gcloud run services describe deepshield-ai --region asia-south1 --format='table(status.url,status.conditions)'
```

---

## 🔄 Update Commands

### Update After Code Changes
```bash
# Quick update
./deploy.sh

# Or manually
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app
gcloud run deploy deepshield-ai --image gcr.io/deepshield-ai/deepshield-app
```

### Update Memory
```bash
gcloud run services update deepshield-ai --memory 4Gi
```

### Update Timeout
```bash
gcloud run services update deepshield-ai --timeout 600
```

### Update CPU
```bash
gcloud run services update deepshield-ai --cpu 4
```

### Update Max Instances
```bash
gcloud run services update deepshield-ai --max-instances 20
```

### Update Min Instances (Keep Warm)
```bash
gcloud run services update deepshield-ai --min-instances 1
```

---

## 🧪 Testing Commands

### Test Health Endpoint
```bash
curl https://[YOUR-URL]/_stcore/health
```

### Test Upload (with curl)
```bash
curl -X POST https://[YOUR-URL] \
  -F "file=@test-image.jpg"
```

### Load Test (10 concurrent requests)
```bash
for i in {1..10}; do
  curl https://[YOUR-URL] &
done
```

---

## 🔍 Debugging Commands

### Check Docker
```bash
docker ps
docker images
```

### Check gcloud Auth
```bash
gcloud auth list
gcloud auth login
```

### Check Project
```bash
gcloud config get-value project
gcloud projects list
```

### Check Region
```bash
gcloud config get-value run/region
```

### View Build History
```bash
gcloud builds list --limit 10
```

### View Specific Build Log
```bash
gcloud builds log [BUILD_ID]
```

### Check Enabled APIs
```bash
gcloud services list --enabled
```

---

## 🗑️ Cleanup Commands

### Delete Service
```bash
gcloud run services delete deepshield-ai --region asia-south1
```

### Delete Images
```bash
gcloud container images list
gcloud container images delete gcr.io/deepshield-ai/deepshield-app
```

### Delete All Builds
```bash
gcloud builds list --format='value(id)' | xargs -I {} gcloud builds cancel {}
```

---

## 💰 Cost Management

### View Current Usage
```bash
gcloud run services describe deepshield-ai --region asia-south1 --format='table(status.url,spec.template.spec.containers[0].resources)'
```

### Set Budget Alert (via Console)
1. Go to: https://console.cloud.google.com/billing
2. Select project: deepshield-ai
3. Set budget alert at $10

### Scale to Zero (Save Costs)
```bash
gcloud run services update deepshield-ai --min-instances 0
```

---

## 🔐 Security Commands

### View IAM Policies
```bash
gcloud run services get-iam-policy deepshield-ai --region asia-south1
```

### Make Service Public
```bash
gcloud run services add-iam-policy-binding deepshield-ai \
  --region asia-south1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

### Make Service Private
```bash
gcloud run services remove-iam-policy-binding deepshield-ai \
  --region asia-south1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

---

## 📦 Local Development

### Run Locally
```bash
streamlit run app.py
```

### Run with Docker Locally
```bash
# Build
docker build -t deepshield-app .

# Run
docker run -p 8080:8080 deepshield-app
```

### Test Docker Build
```bash
docker build -t test-deepshield .
docker run -p 8080:8080 test-deepshield
```

---

## 🔄 Git Commands

### Commit Changes
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Check Status
```bash
git status
git log --oneline -5
```

### Pull Latest
```bash
git pull origin main
```

---

## 🆘 Emergency Commands

### Service Not Responding
```bash
# Check logs
gcloud run logs read deepshield-ai --limit 100

# Restart (redeploy)
gcloud run deploy deepshield-ai --image gcr.io/deepshield-ai/deepshield-app
```

### Out of Memory
```bash
gcloud run services update deepshield-ai --memory 4Gi
```

### Timeout Issues
```bash
gcloud run services update deepshield-ai --timeout 600
```

### Too Many Requests
```bash
gcloud run services update deepshield-ai --max-instances 20
```

### Rollback to Previous Version
```bash
# List revisions
gcloud run revisions list --service deepshield-ai --region asia-south1

# Rollback
gcloud run services update-traffic deepshield-ai \
  --to-revisions [REVISION-NAME]=100 \
  --region asia-south1
```

---

## 📱 Quick Reference

| Task | Command |
|------|---------|
| Deploy | `./deploy.sh` |
| Get URL | `gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)'` |
| View Logs | `gcloud run logs read deepshield-ai --limit 50` |
| Update | `gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app && gcloud run deploy deepshield-ai --image gcr.io/deepshield-ai/deepshield-app` |
| Delete | `gcloud run services delete deepshield-ai --region asia-south1` |

---

## 🎯 Hackathon Submission Commands

### Get Your Links
```bash
# Get the URL
URL=$(gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)')

# Display for submission
echo "MVP Link: $URL"
echo "Working Prototype Link: $URL"
```

### Copy to Clipboard (macOS)
```bash
gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)' | pbcopy
```

### Verify Everything Works
```bash
# 1. Check service is running
gcloud run services describe deepshield-ai --region asia-south1

# 2. Check logs for errors
gcloud run logs read deepshield-ai --limit 20

# 3. Test the URL
curl -I $(gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)')
```

---

**Pro Tip:** Bookmark this file for quick reference during deployment! 🚀

