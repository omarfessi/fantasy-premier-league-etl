if [ -z "$1" ]; then
  echo "Please provide the Cloud Run job name as the first argument, e.g. ./scripts/update_job.sh dbt-modeling-job/ingestion-job"
  exit 1
fi

JOB_NAME="$1"

gcloud run jobs update $JOB_NAME --region=europe-west1