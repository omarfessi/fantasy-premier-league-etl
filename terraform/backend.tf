terraform {
  backend "gcs" {
    bucket = "tf-state-fpl"
    prefix = "terraform/state"
  }
}

# terraform {
#   backend "local" {
#     path = "./terraform.tfstate"
    
#   }
# }