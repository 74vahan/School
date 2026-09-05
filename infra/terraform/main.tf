terraform {
  required_version = ">= 1.7.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

locals {
  labels = {
    project = "school-site"
    env     = var.environment
  }
}

resource "google_compute_network" "vpc" {
  name                    = "school-site-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "school-site-subnet"
  ip_cidr_range = "10.10.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_compute_firewall" "allow_http_https" {
  name    = "allow-http-https"
  network = google_compute_network.vpc.id

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["school-site-app"]
}

resource "google_compute_firewall" "allow_ssh" {
  count   = length(var.allowed_ssh_ranges) > 0 ? 1 : 0
  name    = "allow-ssh"
  network = google_compute_network.vpc.id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = var.allowed_ssh_ranges
  target_tags   = ["school-site-app"]
}

resource "google_compute_address" "app_static_ip" {
  name   = "school-site-static-ip"
  region = var.region
}

# Runs docker compose (app + nginx + db) on boot via cloud-init.
# The compose file and its .env are pulled from the CI/CD deploy step, not baked into the image.
resource "google_compute_instance" "app" {
  name         = "school-site-${var.environment}"
  machine_type = var.machine_type
  tags         = ["school-site-app"]
  labels       = local.labels

  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
      size  = var.app_disk_size_gb
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.subnet.id
    access_config {
      nat_ip = google_compute_address.app_static_ip.address
    }
  }

  metadata = {
    ssh-keys = "app:${file(var.ssh_pub_key_path)}"
  }
}
