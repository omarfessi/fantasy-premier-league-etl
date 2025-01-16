resource "google_storage_bucket" "fantasy_raw_data" {
  name          = "fantasy-raw-data"
  location      = "EU"
  storage_class = "STANDARD"

  force_destroy = true
  project       = "fantasy-premier-league-447918"
  autoclass {
    enabled = true
  }
}
