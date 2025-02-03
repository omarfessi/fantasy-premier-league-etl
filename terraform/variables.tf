variable "fpl_raw_data_bucket_name" {
  description = "The name of the bucket to be created"
  type        = string
  default     = "fantasy-raw-data"

}

variable "sandbox_build" {
  description = "The name of the bucket to be created"
  type        = string
  default     = "fantasy-sandbox-build"
  
}

variable "fpl_dataset_name" {
  description = "The name of the dataset to be created"
  type        = string
  default     = "fantasy_premier_league"

}

variable "services" {
  type = list(string)
  default = [
    "iam.googleapis.com",
    "bigquery.googleapis.com",
    "bigquerystorage.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "eventarc.googleapis.com",
  "run.googleapis.com"]
}

variable "project_level_roles_for_gcf_sa" {
  description = "The roles to grant at the project level"
  type        = list(string)
  default = [
    "roles/run.invoker",
    "roles/eventarc.eventReceiver",
    "roles/artifactregistry.reader",
    "roles/bigquery.jobUser"
  ]
}
variable "storage_level_roles_for_gcf_sa" {
  description = "The roles to grant at the storage level"
  type        = list(string)
  default = [
    "roles/storage.objectViewer"
  ]

}

variable "bq_dataset_level_roles_for_gcf_sa" {
  description = "The roles to grant at the BigQuery Dataset level"
  type        = list(string)
  default = [
    "roles/bigquery.dataEditor"
  ]

}