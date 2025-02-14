#!/bin/bash

# Check if a job name is provided
if [ -z "$1" ]; then
  echo "Please provide the Cloud Run job name as the first argument, e.g. ./scripts/run.sh dbt-modeling-job or ingestion-job"
  exit 1
fi

JOB_NAME="$1"

# Base command
CMD="gcloud beta run jobs execute $JOB_NAME --project='fantasy-open-analytics' --region=europe-west1"

# Conditionally add --update-env-vars if JOB_NAME is "dbt-modeling-job"
if [ "$JOB_NAME" == "dbt-modeling-job" ]; then
  CMD="$CMD --update-env-vars=DBT_GCP_PROJECT=fantasy-open-analytics,DBT_TARGET_DATASET=fantasy_premier_league"
fi

# Execute the final command
echo "Running: $CMD"
eval "$CMD"
