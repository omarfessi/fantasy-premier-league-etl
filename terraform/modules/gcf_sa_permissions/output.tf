output "service_account_email" {
  description = "Email of the created service account that acts on behalf of the cloud function"
  value       = google_service_account.gcf_sa_account.email
}