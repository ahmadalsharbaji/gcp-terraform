# Terraform
terraform {
  backend "gcs" {
    bucket = "gcp-terraform-demo-ax-001-bucket"
    prefix = "terraform/state"
  }
}

# Provider
provider "google" {
  credentials = file("account.json")
  project     = "gcp-terraform-demo-ax-001"
  region      = "us-central1"
}

# Check if the bucket already exists
data "google_storage_bucket" "existing_bucket" {
  name = "gcp-terraform-demo-ax-001-bucket"
}

# Resource for creating the bucket if it does not exist
resource "google_storage_bucket" "my_bucket" {
  count                    = length(data.google_storage_bucket.existing_bucket.*.name) == 0 ? 1 : 0
  name                     = "gcp-terraform-demo-ax-001-bucket"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}
