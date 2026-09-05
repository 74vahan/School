variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "europe-west1-b"
}

variable "environment" {
  description = "Deployment environment (prod, staging, ...)"
  type        = string
  default     = "prod"
}

variable "machine_type" {
  description = "VM machine type for the app/docker host"
  type        = string
  default     = "e2-small"
}

variable "app_disk_size_gb" {
  description = "Boot disk size for the app VM, in GB"
  type        = number
  default     = 30
}

variable "ssh_pub_key_path" {
  description = "Path to the public SSH key allowed to access the VM"
  type        = string
}

variable "allowed_ssh_ranges" {
  description = "CIDR ranges allowed to SSH into the VM"
  type        = list(string)
  default     = []
}
