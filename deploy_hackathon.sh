#!/bin/bash

# ========================================
# GEMINI-3-HACKATHON Deployment Script
# Separate deployment from main project
# ========================================

# Configuration
APP_NAME="gemini3-hackathon"
REGION="us-central1"
REPO_NAME="gemini3-hackathon-repo"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== GEMINI-3-HACKATHON Deployment ===${NC}"

# 1. Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    exit 1
fi

# 2. Get Project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}No default Google Cloud project set.${NC}"
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi
echo -e "Target Project: ${GREEN}${PROJECT_ID}${NC}"

# 3. Enable APIs
echo -e "\n${YELLOW}Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com

# 4. Create Artifact Registry (separate from main project)
echo -e "\n${YELLOW}Checking Artifact Registry...${NC}"
if ! gcloud artifacts repositories describe ${REPO_NAME} --location=${REGION} &> /dev/null; then
    echo "Creating repository ${REPO_NAME}..."
    gcloud artifacts repositories create ${REPO_NAME} \
        --repository-format=docker \
        --location=${REGION} \
        --description="Docker repository for Gemini 3 Hackathon"
else
    echo "Repository ${REPO_NAME} exists."
fi

# 5. Build and Deploy Backend (Hackathon-specific name)
echo -e "\n${GREEN}=== Deploying Hackathon Backend ===${NC}"
BACKEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/backend:latest"

# Get API Key from local env
API_KEY=$(grep GOOGLE_API_KEY backend/app/.env | cut -d '=' -f2)
if [ -z "$API_KEY" ]; then
    echo -e "${RED}Error: GOOGLE_API_KEY not found in backend/app/.env${NC}"
    exit 1
fi

echo "Building Backend Container..."
gcloud builds submit backend --tag ${BACKEND_IMAGE}

echo "Deploying to Cloud Run..."
gcloud run deploy ${APP_NAME}-backend \
    --image ${BACKEND_IMAGE} \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_API_KEY=${API_KEY}" \
    --memory 2Gi \
    --cpu 2

# Capture Backend URL
BACKEND_URL=$(gcloud run services describe ${APP_NAME}-backend --region ${REGION} --format 'value(status.url)')
echo -e "Backend deployed at: ${GREEN}${BACKEND_URL}${NC}"

# 6. Build and Deploy Frontend (Hackathon-specific name)
echo -e "\n${GREEN}=== Deploying Hackathon Frontend ===${NC}"
FRONTEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/frontend:latest"

echo "Building Frontend Container..."
cat > /tmp/cloudbuild-hackathon.yaml << EOF
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '--build-arg'
      - 'BACKEND_URL=${BACKEND_URL}'
      - '-t'
      - '${FRONTEND_IMAGE}'
      - '.'
images:
  - '${FRONTEND_IMAGE}'
EOF

gcloud builds submit frontend --config=/tmp/cloudbuild-hackathon.yaml

echo "Deploying to Cloud Run..."
gcloud run deploy ${APP_NAME}-frontend \
    --image ${FRONTEND_IMAGE} \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "BACKEND_URL=${BACKEND_URL},NEXT_PUBLIC_API_URL=${BACKEND_URL}"

# Capture Frontend URL
FRONTEND_URL=$(gcloud run services describe ${APP_NAME}-frontend --region ${REGION} --format 'value(status.url)')

echo -e "\n${GREEN}=== HACKATHON Deployment Complete! ===${NC}"
echo -e "Frontend: ${GREEN}${FRONTEND_URL}${NC}"
echo -e "Backend:  ${GREEN}${BACKEND_URL}${NC}"
echo -e "Swagger:  ${GREEN}${BACKEND_URL}/docs${NC}"
echo -e "\n${YELLOW}Note: This is a SEPARATE deployment from the main project.${NC}"
echo -e "Service names: ${APP_NAME}-backend, ${APP_NAME}-frontend"
