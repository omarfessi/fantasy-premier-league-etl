variable "project_id" {
  description = "The ID of the project in which to create the resources."
  type        = string
}

variable "region" {
  description = "The region in which to create the resources."
  type        = string
  default     = "europe-west1"
}

variable "function_name" {
  description = "The name of the Cloud Function."
  type        = string
  default     = "load-parquet-to-bq"
}

variable "gcf_local_source_path" {
  description = "The local path to the source code for the Cloud Function."
  type        = string
  default     = "../../../ingestion/load_parquet_to_bq_cf"

}

variable "gcf_zipped_source_path" {
  description = "The path to the zipped source code for the Cloud Function."
  type        = string
  default     = "../../../ingestion/tmp/function.zip"

}

variable "entry_point" {
  description = "The entry point for the Cloud Function."
  type        = string
  default     = "process_gcs_events"
}

variable "service_account_name" {
  description = "The name of the service account the cloud function will use."
  type        = string

}

variable "fpl_raw_data_bucket_name" {
  description = "The name of the staging bucket."
  type        = string
  default     = "fantasy-raw-data"

}

variable "dependency" {
  description = "The dependency of the Cloud Function."
  type        = any

}