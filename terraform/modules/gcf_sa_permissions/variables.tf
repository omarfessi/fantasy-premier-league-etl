variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "fantasy-premier-league-447918"
}

variable "service_account_name" {
  description = "used for both the CF and eventarc trigger to load parquet files to BQ upon GCS notification"
  type        = string
  default     = "parquet-to-bq-gcf-sa"
}

variable "bucket_to_watch" {
  description = "The bucket to watch for GCS notifications"
  type        = string
  default     = "fantasy-raw-data"

}

variable "fpl_dataset_name" {
  description = "The name of the dataset to be created"
  type        = string
}

variable "bucket_resource" {
  description = "Resource reference for the bucket to depend on"
  type        = any
}

variable "project_level_roles" {
  description = "The roles to grant at the project level"
  type        = list(string)
}

variable "storage_level_roles" {
  description = "The roles to grant at the storage level"
  type        = list(string)
}

variable "bq_dataset_level_roles" {
  description = "The roles to grant at the bq dataset level"
  type        = list(string)
}