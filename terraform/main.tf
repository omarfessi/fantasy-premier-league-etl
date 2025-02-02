#create a bucket to store the raw data 
#and give the default gcs service account the permission to publish to pubsub
resource "google_storage_bucket" "fantasy_raw_data" {
  name          = var.fpl_raw_data_bucket_name
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"
  force_destroy = false
  versioning {
    enabled = true
  }
}
#give the default sa the permission to publish to pubsub (for notifications)
data "google_storage_project_service_account" "default" {
}

resource "google_project_iam_member" "gcs_pubsub_publishing" {
  project = local.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.default.email_address}"
}

resource "google_bigquery_dataset" "fpl_dataset" {
  project                    = local.project_id
  dataset_id                 = var.fpl_dataset_name
  description                = "This is a dataset for storing fantasy premier league data"
  location                   = local.region
  delete_contents_on_destroy = true
}


#create a service account for the cloud function with the necessary project permissions 
#to invoke the function,
#receive events from eventarc,
#read artifacts from artifact registry, 
#and resource permissions to
#write to bigquery ( user and data editor roles)
module "gcf_service_account_creation_with_permissions" {
  source                 = "./modules/gcf_sa_permissions"
  fpl_dataset_name       = google_bigquery_dataset.fpl_dataset.dataset_id
  bucket_resource        = google_storage_bucket.fantasy_raw_data
  project_level_roles    = var.project_level_roles_for_gcf_sa
  storage_level_roles    = var.storage_level_roles_for_gcf_sa
  bq_dataset_level_roles = var.bq_dataset_level_roles_for_gcf_sa


}
module "load_parquet_to_bq_cf_creation" {
  source                   = "./modules/gcf_creation"
  project_id               = local.project_id
  region                   = local.region
  function_name            = "load-parquet-to-bq"
  gcf_local_source_path    = "../ingestion/load_parquet_to_bq_cf"
  gcf_zipped_source_path   = "./tmp/function.zip"
  entry_point              = "process_gcs_events"
  service_account_name     = module.gcf_service_account_creation_with_permissions.service_account_email
  fpl_raw_data_bucket_name = var.fpl_raw_data_bucket_name
  dependency               = module.gcf_service_account_creation_with_permissions

}


resource "google_cloud_run_v2_job" "dbt_modeling_job" {
  name     = "dbt-modeling-job"
  location = local.region
  deletion_protection = false

  template {
    template {
      containers {
        image = "${local.region}-docker.pkg.dev/${local.project_id}/${local.repo_name}/${local.image_name}:${local.image_tag}"
      }
    }
  }
}