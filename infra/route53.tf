# Route 53 Hosted Zone for domain
# NOTE: After applying, update nameservers at your domain registrar

resource "aws_route53_zone" "main" {
  name    = var.domain_name
  comment = "Hosted zone for ${var.domain_name}"

  tags = {
    Name        = var.domain_name
    Environment = var.environment
  }
}

# DNS record for frontend (shop.higuera.io -> CloudFront)
resource "aws_route53_record" "frontend" {
  zone_id = aws_route53_zone.main.zone_id
  name    = local.full_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

# DNS record for API (api.shop.higuera.io -> API Gateway)
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = local.api_domain
  type    = "A"

  alias {
    name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

# Output nameservers - you'll need to update these at your registrar
output "nameservers" {
  description = "Update these nameservers at your domain registrar"
  value       = aws_route53_zone.main.name_servers
}
