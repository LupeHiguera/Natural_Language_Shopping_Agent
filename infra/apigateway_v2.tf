# API Gateway v2 (HTTP API) - Cheaper than REST API

resource "aws_apigatewayv2_api" "api" {
  name          = "shop-api"
  protocol_type = "HTTP"
  description   = "HTTP API for shoe shopping backend"

  cors_configuration {
    allow_origins     = ["https://${local.full_domain}"]
    allow_methods     = ["GET", "POST", "OPTIONS"]
    allow_headers     = ["Content-Type", "Authorization"]
    allow_credentials = true
    max_age           = 3600
  }

  tags = {
    Name        = "shop-api"
    Environment = var.environment
  }
}

# Lambda integration
resource "aws_apigatewayv2_integration" "api" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.api.invoke_arn
  payload_format_version = "2.0"
}

# Default route - catch all
resource "aws_apigatewayv2_route" "api" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}

# Stage
resource "aws_apigatewayv2_stage" "api" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      responseLength = "$context.responseLength"
      errorMessage   = "$context.error.message"
    })
  }

  tags = {
    Name        = "shop-api-stage"
    Environment = var.environment
  }
}

# CloudWatch log group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/shop-api"
  retention_in_days = 7  # Keep logs for 7 days to minimize costs

  tags = {
    Name        = "shop-api-logs"
    Environment = var.environment
  }
}

# Custom domain for API
resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = local.api_domain

  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.main.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  tags = {
    Name        = local.api_domain
    Environment = var.environment
  }
}

# Map custom domain to API stage
resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = aws_apigatewayv2_api.api.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.api.id
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = "https://${local.api_domain}"
}

output "api_gateway_url" {
  description = "API Gateway default URL (before custom domain is set up)"
  value       = aws_apigatewayv2_api.api.api_endpoint
}
