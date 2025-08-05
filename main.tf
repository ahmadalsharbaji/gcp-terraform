terraform {
  backend "gcs" {
    bucket = "gcp-terraform-demo-ax-001-bucket"
    prefix = "terraform/state"
  }
}

provider "google" {
  credentials = file("account.json")
  project     = "gcp-terraform-demo-ax-001"
  region      = "us-central1"
}

resource "google_storage_bucket" "my_bucket" {
  name                     = "gcp-terraform-demo-ax-001-bucket"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}
