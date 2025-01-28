#prepare the name of the bucket that will hold the source code of the cloud function
resource "random_id" "bucket_prefix" {
  byte_length = 8
}
# Create a bucket to store the source code for the cloud function
resource "google_storage_bucket" "gcf_source_bucket" {
  name          = "${random_id.bucket_prefix.hex}-gcf-source-bucket"
  project       = var.project_id
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true
  versioning {
    enabled = true
  }
}
#archive the source code
data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.gcf_local_source_path
  output_path = var.gcf_zipped_source_path
}

#upload the source code to the bucket
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
resource "google_cloudfunctions2_function" "default" {
  name        = var.function_name
  location    = var.region
  description = "This function loads parquet files to BigQuery tables on GCS notification"
  depends_on = [
    var.dependency
  ]

  build_config {
    runtime     = "python312"
    entry_point = var.entry_point
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
    service_account_email          = var.service_account_name
  }
  event_trigger {
    trigger_region        = var.region # The trigger must be in the same location as the bucket
    event_type            = "google.cloud.storage.object.v1.finalized"
    retry_policy          = "RETRY_POLICY_RETRY"
    service_account_email = var.service_account_name
    event_filters {
      attribute = "bucket"
      value     = var.fpl_raw_data_bucket_name
    }
  }

}