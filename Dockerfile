FROM ghcr.io/dbt-labs/dbt-bigquery:1.9.0
WORKDIR /app
COPY modeling/ .
ENTRYPOINT ["dbt", "run", "--profiles-dir", ".", "--project-dir", "." ]

# after building the image run 
# docker run --rm --env-file .env -v ~/.config/gcloud:/root/.config/gcloud dbt-runner