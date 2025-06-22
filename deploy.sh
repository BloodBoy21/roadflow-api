#!/bin/bash

set -e  # Exit on any error

# === Config ===
REGION="us-west1"
PROJECT_ID="manifest-grin-462423-m3"
REPO_NAME="hackaton"
SERVICE_NAME="flow-api"
LOCAL_IMAGE="bloodbloy/${SERVICE_NAME}"
REMOTE_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"

# === Build ===
echo "🔨 Building Docker image..."
docker buildx build --platform linux/amd64 -t $LOCAL_IMAGE . --no-cache

# === Tag ===
echo "🏷️ Tagging image for Artifact Registry..."
docker tag $LOCAL_IMAGE $REMOTE_IMAGE

# === Push ===
echo "📤 Pushing image to Artifact Registry..."
docker push $REMOTE_IMAGE

# === Deploy ===
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $REMOTE_IMAGE \
  --region $REGION \
  --allow-unauthenticated \
  --env-vars-file .env.yaml \
  --memory 2Gi \
  --cpu 2 \
  --project $PROJECT_ID

echo "✅ Deployment completed successfully."
