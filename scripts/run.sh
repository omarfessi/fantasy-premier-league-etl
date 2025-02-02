#This to run the dbt modeling job on GCP Cloud Run
#TODO: Automate this execution. Currently, it is manual
gcloud beta run jobs execute dbt-modeling-job \
    --project="fantasy-premier-league-447918" \
    --region=europe-west1 \
    --update-env-vars=DBT_GCP_PROJECT=fantasy-premier-league-447918,DBT_TARGET_DATASET=fantasy_premier_league
