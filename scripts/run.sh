#This to run the dbt modeling job on GCP Cloud Run
#TODO: Automate this execution. Currently, it is manual
gcloud beta run jobs execute dbt-modeling-job \
    --project="fantasy-open-analytics" \
    --region=europe-west1 \
    --update-env-vars=DBT_GCP_PROJECT=fantasy-open-analytics,DBT_TARGET_DATASET=fantasy_premier_league
