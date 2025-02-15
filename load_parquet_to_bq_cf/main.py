import functions_framework
from google.cloud import bigquery


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def process_gcs_events(cloud_event):
    data = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"File {file_name} uploaded to bucket {bucket_name}.")

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    if (
        file_name.startswith("fixtures")
        or file_name.startswith("elements")
        or file_name.startswith("events")
        or file_name.startswith("teams")
    ):
        table_id = f"fantasy-open-analytics.fantasy_premier_league.raw_{file_name.split('_')[0]}"
        uri = f"gs://fantasy-raw-data/{file_name}"
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        load_job.result()  # Waits for the job to complete.
        destination_table = client.get_table(table_id)
        print(f"Loaded {destination_table.num_rows} rows into {table_id}.")
