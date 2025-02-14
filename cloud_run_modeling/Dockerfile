FROM ghcr.io/dbt-labs/dbt-bigquery:1.9.0

WORKDIR /app

# Copy the necessary files for dbt
COPY modeling/ .

# Install dependencies before running dbt
RUN dbt deps --profiles-dir . --project-dir .

# Run dbt when the container starts
ENTRYPOINT ["dbt", "run", "--profiles-dir", ".", "--project-dir", "."]

# after building the image run (docker build -t dbt-runner . )
# docker run --rm --env-file .env -v ~/.config/gcloud:/root/.config/gcloud dbt-runner
