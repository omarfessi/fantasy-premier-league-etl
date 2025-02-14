resource "google_project_service" "services" {
  for_each                   = toset(var.services)
  project                    = local.project_id
  service                    = each.key
  disable_dependent_services = true
}
#create a bucket to store the raw data 
#and give the default gcs service account the permission to publish to pubsub
resource "google_storage_bucket" "fantasy_raw_data" {
  name          = var.fpl_raw_data_bucket_name
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"
  force_destroy = true
  versioning {
    enabled = true
  }
  depends_on = [google_project_service.services]
}
#give the default sa the permission to publish to pubsub (for notifications)
data "google_storage_project_service_account" "default" {
  project = local.project_id
}

resource "google_project_iam_member" "gcs_pubsub_publishing" {
  project    = local.project_id
  role       = "roles/pubsub.publisher"
  member     = "serviceAccount:${data.google_storage_project_service_account.default.email_address}"
  depends_on = [google_project_service.services]
}

resource "google_bigquery_dataset" "fpl_dataset" {
  project                    = local.project_id
  dataset_id                 = var.fpl_dataset_name
  description                = "This is a dataset for storing fantasy premier league data"
  location                   = local.region
  delete_contents_on_destroy = true
  depends_on                 = [google_project_service.services]
}


#create a service account for the cloud function with the necessary project permissions 
#to invoke the function,
#receive events from eventarc,
#read artifacts from artifact registry, 
#and resource permissions to
#write to bigquery ( user and data editor roles)
module "gcf_service_account_creation_with_permissions" {
  source                 = "./modules/gcf_sa_permissions"
  project_id             = local.project_id
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
  gcf_local_source_path    = "../load_parquet_to_bq_cf"
  gcf_zipped_source_path   = "./tmp/function.zip"
  entry_point              = "process_gcs_events"
  service_account_name     = module.gcf_service_account_creation_with_permissions.service_account_email
  fpl_raw_data_bucket_name = var.fpl_raw_data_bucket_name
  dependency               = [module.gcf_service_account_creation_with_permissions, google_project_service.services]

}

resource "google_service_account" "dbt_modeling_gcrj_sa" {
  account_id   = "dbt-modeling-gcrj-sa"
  display_name = "Service Account used by the dbt modeling job"
}

resource "google_project_iam_member" "bq_job_user" {
  project = local.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dbt_modeling_gcrj_sa.email}"
}

resource "google_bigquery_dataset_iam_member" "bigquery_dataset_data_editor_gcrj_sa" {
  dataset_id = var.fpl_dataset_name
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.dbt_modeling_gcrj_sa.email}"
  depends_on = [google_bigquery_dataset.fpl_dataset]
}

resource "google_artifact_registry_repository" "omars_container_repo" {
  location      = local.region
  repository_id = local.repo_name
  description   = "Docker repository for storing container images"
  format        = "DOCKER"
  depends_on    = [google_project_service.services]
}

resource "google_storage_bucket" "fantasy_sandbox_build" {

  name          = var.sandbox_build
  project       = local.project_id
  location      = local.region
  storage_class = "STANDARD"
  force_destroy = true
  
}


resource "null_resource" "build_docker_image" {
  provisioner "local-exec" {
    command     = "scripts/cloud_build.sh"
    working_dir = "../"

  }
  depends_on = [google_artifact_registry_repository.omars_container_repo, google_storage_bucket.fantasy_sandbox_build]

}

#TODO: add sandboxing for the dbt modeling job

data "google_artifact_registry_docker_image" "gcrj_image" {
  location      = google_artifact_registry_repository.omars_container_repo.location
  repository_id = google_artifact_registry_repository.omars_container_repo.repository_id
  image_name    = "modeling-dbt:latest"
  depends_on    = [null_resource.build_docker_image]
}


output "image_name" {
  value = data.google_artifact_registry_docker_image.gcrj_image.name

}

resource "google_cloud_run_v2_job" "dbt_modeling_job" {
  name                = "dbt-modeling-job"
  location            = local.region
  deletion_protection = false
  depends_on          = [data.google_artifact_registry_docker_image.gcrj_image, google_project_service.services]

  template {
    template {
      containers {
        image = "${local.region}-docker.pkg.dev/${local.project_id}/${local.repo_name}/${local.image_name}:${local.image_tag}"
      }
      service_account = google_service_account.dbt_modeling_gcrj_sa.email
    }
  }
}

## Ingestion job

resource "google_service_account" "ingestion_gcrj_sa" {
  account_id   = "ingestion-gcrj-sa"
  display_name = "Service Account used by the ingestion job"
}

resource "google_storage_bucket_iam_member" "ingestion_gcs_sa_writer" {
  bucket = google_storage_bucket.fantasy_raw_data.name
  role = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.ingestion_gcrj_sa.email}"
}


resource "google_cloud_run_v2_job" "ingestion_job" {
  name                = "ingestion-job"
  location            = local.region
  deletion_protection = false
  depends_on          = [ google_project_service.services]

  template {
    template {
      containers {
        image = "${local.region}-docker.pkg.dev/${local.project_id}/${local.repo_name}/ingestion:${local.image_tag}"
      }
      service_account = google_service_account.ingestion_gcrj_sa.email
    }
  }
}