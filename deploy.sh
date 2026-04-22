#!/bin/bash

# DeepShield AI - Cloud Run Deployment Script
# Run this script from the project root directory

set -e  # Exit on error

echo "🛡️  DeepShield AI - Cloud Run Deployment"
echo "========================================"
echo ""

# Configuration
PROJECT_ID="deepshield-ai"
REGION="asia-south1"
SERVICE_NAME="deepshield-ai"
IMAGE_NAME="gcr.io/${PROJECT_ID}/deepshield-app"

# Step 1: Fix permissions (if needed)
echo "📋 Step 1: Checking gcloud permissions..."
if [ ! -w ~/.config/gcloud ]; then
    echo "⚠️  Fixing gcloud permissions..."
    sudo chown -R $(whoami) ~/.config/gcloud 2>/dev/null || true
fi
echo "✅ Permissions OK"
echo ""

# Step 2: Set project
echo "📋 Step 2: Setting project..."
gcloud config set project ${PROJECT_ID}
echo "✅ Project set to ${PROJECT_ID}"
echo ""

# Step 3: Set region
echo "📋 Step 3: Setting region..."
gcloud config set run/region ${REGION}
echo "✅ Region set to ${REGION}"
echo ""

# Step 4: Enable APIs
echo "📋 Step 4: Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo "✅ APIs enabled"
echo ""

# Step 5: Build image
echo "📋 Step 5: Building Docker image..."
echo "⏳ This may take 5-10 minutes..."
gcloud builds submit --tag ${IMAGE_NAME}
echo "✅ Image built successfully"
echo ""

# Step 6: Deploy to Cloud Run
echo "📋 Step 6: Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📝 Getting service URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')
echo ""
echo "✅ Your DeepShield AI app is live at:"
echo "🔗 ${SERVICE_URL}"
echo ""
echo "📋 Next Steps:"
echo "1. Open the URL in your browser"
echo "2. Test by uploading an image or video"
echo "3. Copy the URL for your hackathon submission"
echo ""
echo "💡 Useful Commands:"
echo "   View logs: gcloud run logs read ${SERVICE_NAME} --limit 50"
echo "   Update app: ./deploy.sh (run this script again)"
echo "   Delete app: gcloud run services delete ${SERVICE_NAME} --region ${REGION}"
echo ""
