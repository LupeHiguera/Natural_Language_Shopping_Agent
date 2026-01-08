# Lambda Function for FastAPI Backend

# IAM Role for API Lambda
resource "aws_iam_role" "api_lambda" {
  name = "shop-api-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "api_lambda_basic" {
  role       = aws_iam_role.api_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy for DynamoDB access
resource "aws_iam_role_policy" "api_lambda_dynamodb" {
  name = "dynamodb-access"
  role = aws_iam_role.api_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.shoe-inventory-table.arn,
          "${aws_dynamodb_table.shoe-inventory-table.arn}/index/*"
        ]
      }
    ]
  })
}

# Policy for Bedrock Agent access
resource "aws_iam_role_policy" "api_lambda_bedrock" {
  name = "bedrock-access"
  role = aws_iam_role.api_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeAgent"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda function for API
resource "aws_lambda_function" "api" {
  filename         = "${path.module}/../backend/lambda_package.zip"
  function_name    = "shop-api"
  role             = aws_iam_role.api_lambda.arn
  handler          = "lambda_handler.handler"
  runtime          = "python3.11"
  timeout          = 30
  memory_size      = 512

  environment {
    variables = {
      DYNAMODB_TABLE_NAME    = aws_dynamodb_table.shoe-inventory-table.name
      BEDROCK_AGENT_ID       = var.bedrock_agent_id
      BEDROCK_AGENT_ALIAS_ID = var.bedrock_agent_alias_id
      AWS_REGION_NAME        = var.aws_region
      MOCK_MODE              = "false"
      CORS_ORIGINS_STR       = "https://${local.full_domain}"
    }
  }

  tags = {
    Name        = "shop-api"
    Environment = var.environment
  }
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
