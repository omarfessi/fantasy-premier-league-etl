terraform {
  backend "gcs" {
    bucket = "tf-state-fpl"
    prefix = "terraform/state"
  }
}

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