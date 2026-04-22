# 🚀 DeepShield AI - Deployment Guide

## Quick Links

### 🔗 Live Application Links

**MVP Link (Minimum Viable Product):**
```
https://deepshield-ai-[hash]-uc.a.run.app
```
*Will be generated after deployment*

**Working Prototype Link:**
```
https://deepshield-ai-[hash]-uc.a.run.app
```
*Same as MVP - fully functional production deployment*

---

## Prerequisites

### 1. Install Google Cloud SDK
```bash
# macOS
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize gcloud
gcloud init
```

### 2. Install Docker Desktop
```bash
# macOS (Homebrew)
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

### 3. Verify Installation
```bash
gcloud --version
docker --version
```

---

## Deployment Steps

### Step 1: Configure Google Cloud Project
```bash
# Set project ID
gcloud config set project deepshield-ai

# Set default region
gcloud config set run/region asia-south1

# Authenticate
gcloud auth login
gcloud auth configure-docker
```

### Step 2: Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 3: Build Docker Image
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app

# This will:
# - Build the Docker image from Dockerfile
# - Push to Google Container Registry
# - Take ~5-10 minutes
```

### Step 4: Deploy to Cloud Run
```bash
gcloud run deploy deepshield-ai \
  --image gcr.io/deepshield-ai/deepshield-app \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0
```

### Step 5: Get Your Live URL
```bash
# After deployment completes, you'll see:
Service [deepshield-ai] revision [deepshield-ai-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://deepshield-ai-[hash]-uc.a.run.app
```

**Copy this URL - this is your MVP and Working Prototype link!**

---

## One-Command Deployment

```bash
# Run everything in one go
gcloud config set project deepshield-ai && \
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com && \
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app && \
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

---

## Testing Your Deployment

### 1. Open the URL in Browser
```
https://deepshield-ai-[your-hash]-uc.a.run.app
```

### 2. Test Upload
- Upload a sports image or video
- Wait for analysis (3-5 seconds)
- Verify results and certificate generation

### 3. Health Check
```bash
curl https://deepshield-ai-[your-hash]-uc.a.run.app/_stcore/health
```

---

## Configuration

### Environment Variables (Optional)
If you need to add environment variables:

```bash
gcloud run services update deepshield-ai \
  --set-env-vars="KEY1=value1,KEY2=value2"
```

### Update Deployment
```bash
# After code changes
gcloud builds submit --tag gcr.io/deepshield-ai/deepshield-app
gcloud run deploy deepshield-ai --image gcr.io/deepshield-ai/deepshield-app
```

### View Logs
```bash
gcloud run logs read deepshield-ai --limit 50
```

### Delete Deployment
```bash
gcloud run services delete deepshield-ai --region asia-south1
```

---

## Troubleshooting

### Issue: Build Fails
```bash
# Check build logs
gcloud builds list --limit 5
gcloud builds log [BUILD_ID]
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

### Issue: Cold Start Slow
```bash
# Set minimum instances
gcloud run services update deepshield-ai --min-instances 1
```

---

## Cost Optimization

### Free Tier Limits
- 2 million requests/month
- 360,000 GB-seconds/month
- 180,000 vCPU-seconds/month

### Reduce Costs
```bash
# Set max instances
gcloud run services update deepshield-ai --max-instances 5

# Set min instances to 0 (scale to zero)
gcloud run services update deepshield-ai --min-instances 0
```

---

## Production Checklist

- [x] Dockerfile created
- [x] .dockerignore configured
- [x] Health check endpoint
- [x] CORS disabled for Cloud Run
- [x] Port 8080 configured
- [x] Memory optimized (2Gi)
- [x] Timeout set (300s)
- [ ] Custom domain (optional)
- [ ] SSL certificate (auto-provisioned)
- [ ] Monitoring enabled
- [ ] Logging configured

---

## Custom Domain (Optional)

### 1. Verify Domain
```bash
gcloud domains verify example.com
```

### 2. Map Domain
```bash
gcloud run domain-mappings create \
  --service deepshield-ai \
  --domain deepshield.example.com \
  --region asia-south1
```

### 3. Update DNS
Add the provided DNS records to your domain registrar.

---

## Monitoring & Alerts

### View Metrics
```bash
# Open Cloud Console
gcloud run services describe deepshield-ai --region asia-south1
```

### Set Up Alerts
1. Go to Cloud Console → Monitoring
2. Create alert for:
   - Request count > 1000/min
   - Error rate > 5%
   - Latency > 10s

---

## Support

**Issues?**
- Check logs: `gcloud run logs read deepshield-ai`
- View metrics: Cloud Console → Cloud Run → deepshield-ai
- GitHub: https://github.com/sahithirithvika/deepshield-ai

**Need Help?**
- Google Cloud Support: https://cloud.google.com/support
- Streamlit Docs: https://docs.streamlit.io/deploy/streamlit-community-cloud

---

## Summary

After successful deployment, you will have:

✅ **MVP Link**: `https://deepshield-ai-[hash]-uc.a.run.app`
✅ **Working Prototype**: Same URL (fully functional)
✅ **Auto-scaling**: 0 to 10 instances
✅ **Global CDN**: Fast worldwide access
✅ **HTTPS**: Auto SSL certificate
✅ **99.95% SLA**: Production-grade reliability

**Deployment Time**: ~10-15 minutes
**Cost**: Free tier covers most usage

---

*Last Updated: 2026-04-18*
