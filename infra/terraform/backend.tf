terraform {
  backend "gcs" {
    bucket = "school-site-tfstate" # create this bucket manually once, outside Terraform
    prefix = "terraform/state"
  }
}
