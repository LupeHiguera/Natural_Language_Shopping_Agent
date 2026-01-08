# Variables for deployment configuration

variable "domain_name" {
  description = "Root domain name"
  type        = string
  default     = "higuera.io"
}

variable "subdomain" {
  description = "Subdomain for the shopping app"
  type        = string
  default     = "shop"
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

# Bedrock Agent Configuration (from existing setup)
variable "bedrock_agent_id" {
  description = "Bedrock Agent ID"
  type        = string
  default     = "QTQ1JQCBEW"
}

variable "bedrock_agent_alias_id" {
  description = "Bedrock Agent Alias ID"
  type        = string
  default     = "HQTVGQMY41"
}

# Computed locals
locals {
  full_domain     = "${var.subdomain}.${var.domain_name}"
  api_domain      = "api.${var.subdomain}.${var.domain_name}"
  s3_bucket_name  = "${var.subdomain}-${replace(var.domain_name, ".", "-")}-frontend"
}
