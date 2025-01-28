resource "google_service_account" "gcf_sa_account" {
  account_id   = var.service_account_name
  display_name = "used for both the CF and eventarc trigger to load parquet files to BQ upon GCS notification"
}
resource "google_project_iam_member" "project_level_roles" {
  project  = var.project_id
  for_each = toset(var.project_level_roles)
  role     = each.key
  member   = "serviceAccount:${google_service_account.gcf_sa_account.email}"
}

resource "google_storage_bucket_iam_member" "storage_object_viewer" {
  bucket     = var.bucket_to_watch
  for_each   = toset(var.storage_level_roles)
  role       = each.key
  member     = "serviceAccount:${google_service_account.gcf_sa_account.email}"
  depends_on = [var.bucket_resource]

}


resource "google_bigquery_dataset_iam_member" "bigquery_dataset_data_editor" {
  dataset_id = var.fpl_dataset_name
  for_each   = toset(var.bq_dataset_level_roles)
  role       = each.key
  member     = "serviceAccount:${google_service_account.gcf_sa_account.email}"
}