PROJECT_ID="fantasy-open-analytics"
REGION="europe-west1"
IMAGE_NAME="modeling-dbt"
IMAGE_TAG="latest"
REPO_NAME="omars-containers"
SDK_DOCKERFILE_PATH="./Dockerfile"
BUILD_STAGIN_LOCATION="gs://fantasy-sandbox-build/staging"
BUILD_LOGS_LOCATION="gs://fantasy-sandbox-build/logs"

gcloud builds submit \
    --config=cloudbuild.yaml \
    --project=$PROJECT_ID \
    --gcs-log-dir=$BUILD_LOGS_LOCATION \
    --gcs-source-staging-dir=$BUILD_STAGIN_LOCATION \
    --substitutions=_PROJECT_ID=$PROJECT_ID,_REGION=$REGION,_IMAGE_NAME=$IMAGE_NAME,_IMAGE_TAG=$IMAGE_TAG,_REPO_NAME=$REPO_NAME
