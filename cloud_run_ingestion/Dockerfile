FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire ingestion folder into the container
COPY ingestion/ ingestion/ 

# Don't forget to mount the service account key file when running the container
# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json"

# Set the entrypoint (modify as needed)
CMD ["python", "-m", "ingestion.pipeline"]

# docker run --rm \
#     -v ./fantasy-open-analytics-service-account.json:/app/service-account.json \
#     fpl-ingestion-pipeline