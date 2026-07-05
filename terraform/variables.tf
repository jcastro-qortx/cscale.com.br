variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket name for the website"
  type        = string
  default     = "cscale-website"
}

variable "domain_name" {
  description = "Custom domain for the site"
  type        = string
  default     = "site.corescale.com.br"
}

variable "contact_email" {
  description = "Email address to receive contact form submissions"
  type        = string
  default     = "jcastro@cscale.com.br"
}

variable "sender_email" {
  description = "Email address used as sender (must be verified in SES)"
  type        = string
  default     = "site@cscale.com.br"
}
