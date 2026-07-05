output "website_url" {
  description = "S3 bucket regional domain (access via CloudFront only)"
  value       = aws_s3_bucket.website.bucket_regional_domain_name
}

output "cloudfront_url" {
  description = "CloudFront distribution URL"
  value       = "https://${aws_cloudfront_distribution.site.domain_name}"
}

output "custom_domain_url" {
  description = "Custom domain URL (after DNS setup)"
  value       = "https://${var.domain_name}"
}

output "dns_cname_record" {
  description = "CNAME record to create in the DNS account: site.corescale.com.br -> CloudFront"
  value       = "${var.domain_name} -> ${aws_cloudfront_distribution.site.domain_name}"
}

output "acm_validation_records" {
  description = "DNS records to create for ACM certificate validation"
  value = {
    for dvo in aws_acm_certificate.site.domain_validation_options : dvo.domain_name => {
      type  = dvo.resource_record_type
      name  = dvo.resource_record_name
      value = dvo.resource_record_value
    }
  }
}

output "contact_api_url" {
  description = "API Gateway URL for the contact form"
  value       = "${aws_apigatewayv2_stage.default.invoke_url}/contact"
}

output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.website.id
}

output "ses_verification_status" {
  description = "SES email identity verification - check AWS console to confirm"
  value       = "Verification emails sent to ${var.contact_email} (recipient) and ${var.sender_email} (sender). Confirm BOTH via email link."
}
