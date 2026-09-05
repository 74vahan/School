output "app_external_ip" {
  description = "Static external IP of the app VM"
  value       = google_compute_address.app_static_ip.address
}

output "app_instance_name" {
  description = "Name of the app VM instance"
  value       = google_compute_instance.app.name
}
