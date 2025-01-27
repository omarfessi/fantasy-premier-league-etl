resource "google_storage_bucket" "tf-state-fpl" {
  name          = "tf-state-fpl"
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"
  force_destroy = false
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "fantasy_raw_data" {
  name          = "fantasy-raw-data"
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"

  force_destroy = true
}
resource "random_id" "bucket_prefix" {
  byte_length = 8
}
resource "google_storage_bucket" "gcf_source_bucket" {
  name          = "${random_id.bucket_prefix.hex}-gcf-source-bucket"
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"
  force_destroy = true
  versioning {
    enabled = true
  }

}
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../ingestion/load_parquet_to_bq_cf"
  output_path = "./tmp/function.zip"
}

resource "google_storage_bucket_object" "object" {
  name         = "src-${data.archive_file.source.output_md5}.zip"
  bucket       = google_storage_bucket.gcf_source_bucket.name
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  depends_on = [
    google_storage_bucket.gcf_source_bucket,
    data.archive_file.source
  ]
}

data "google_storage_project_service_account" "default" {
}

resource "google_project_iam_member" "gcs_pubsub_publishing" {
  project = data.google_project.project.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.default.email_address}"
}

data "google_project" "project" {
}

resource "google_service_account" "account" {
  account_id   = "parquet-to-bq-gcf-sa"
  display_name = "Service Account - used for both the cloud function and eventarc trigger in the test"
}

# Permissions on the service account used by the function and Eventarc trigger
resource "google_project_iam_member" "invoking" {
  # project    = data.google_project.project.project_id
  project    = local.project_id
  role       = "roles/run.invoker"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.gcs_pubsub_publishing]
}

resource "google_project_iam_member" "event_receiving" {
  project    = local.project_id
  role       = "roles/eventarc.eventReceiver"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.invoking]
}

resource "google_project_iam_member" "artifactregistry_reader" {
  project    = local.project_id
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.event_receiving]
}

resource "google_project_iam_member" "bigquery_job_user" {
  project = local.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.account.email}"
}

resource "google_project_iam_member" "bigquery_data_editor" {
  project = local.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.account.email}"
}

resource "google_storage_bucket_iam_member" "storage_object_viewer" {
  bucket = google_storage_bucket.fantasy_raw_data.name
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.account.email}"
}

resource "google_cloudfunctions2_function" "default" {
  name        = "load-parquet-to-bq"
  location    = local.region
  description = "This function loads parquet files to BigQuery tables on GCS notification"
  depends_on = [
    google_project_iam_member.event_receiving,
    google_project_iam_member.artifactregistry_reader,
  ]

  build_config {
    runtime     = "python312"
    entry_point = "process_gcs_events"
    source {
      storage_source {
        bucket = google_storage_bucket.gcf_source_bucket.name
        object = google_storage_bucket_object.object.name
      }
    }
  }
  service_config {
    max_instance_count             = 3
    min_instance_count             = 1
    available_memory               = "256M"
    timeout_seconds                = 60
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = google_service_account.account.email
  }
  event_trigger {
    trigger_region        = local.region # The trigger must be in the same location as the bucket
    event_type            = "google.cloud.storage.object.v1.finalized"
    retry_policy          = "RETRY_POLICY_RETRY"
    service_account_email = google_service_account.account.email
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.fantasy_raw_data.name
    }
  }

}

resource "google_bigquery_dataset" "fpl_dataset" {
  project                    = local.project_id
  dataset_id                 = "fantasy_premier_league"
  description                = "This is a dataset for storing fantasy premier league data"
  location                   = local.region
  delete_contents_on_destroy = true
}