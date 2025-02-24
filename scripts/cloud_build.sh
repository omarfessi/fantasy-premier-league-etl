#!/bin/bash

# Ensure IMAGE_NAME is set
if [ -z "$1" ]; then
  echo "Please provide the IMAGE_NAME as the first argument, e.g. ./scripts/cloud_build.sh modeling-dbt/ingestion"
  exit 1
fi

IMAGE_NAME=$1

# Define other variables
PROJECT_ID="fantasy-open-analytics"
REGION="europe-west1"
IMAGE_TAG="latest"
REPO_NAME="omars-containers"
BUILD_STAGING_LOCATION="gs://fantasy-sandbox-build/staging"
BUILD_LOGS_LOCATION="gs://fantasy-sandbox-build/logs"

# Set the correct build path based on the image name
if [ "$IMAGE_NAME" == "modeling-dbt" ]; then
  BUILD_CONTEXT="cloud_run_modeling/"
elif [ "$IMAGE_NAME" == "ingestion" ]; then
  BUILD_CONTEXT="cloud_run_ingestion/"
else
  echo "Invalid IMAGE_NAME provided. Use 'modeling-dbt' or 'ingestion'."
  exit 1
fi

# Submit the build
gcloud builds submit \
    --config=cloudbuild.yaml \
    --project=$PROJECT_ID \
    --gcs-log-dir=$BUILD_LOGS_LOCATION \
    --gcs-source-staging-dir=$BUILD_STAGING_LOCATION \
    --substitutions=_PROJECT_ID=$PROJECT_ID,_REGION=$REGION,_IMAGE_NAME=$IMAGE_NAME,_IMAGE_TAG=$IMAGE_TAG,_REPO_NAME=$REPO_NAME,_BUILD_CONTEXT=$BUILD_CONTEXT
