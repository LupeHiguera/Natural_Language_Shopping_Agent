resource "aws_api_gateway_rest_api" "shoe_api"{
  name = "shoe_api"
  description = "Allows for the lambda function to connect to the api gateway"
}

resource "aws_api_gateway_resource" "search_shoes"{
  parent_id   = aws_api_gateway_rest_api.shoe_api.root_resource_id
  path_part   = "search"
  rest_api_id = aws_api_gateway_rest_api.shoe_api.id
}

resource "aws_api_gateway_method" "search_shoes_method"{
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.search_shoes.id
  rest_api_id   = aws_api_gateway_rest_api.shoe_api.id
}

resource "aws_api_gateway_integration" "search_shoes_gateway"{
  rest_api_id = aws_api_gateway_rest_api.shoe_api.id
  resource_id = aws_api_gateway_resource.search_shoes.id
  http_method = "POST"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.search_shoes.invoke_arn
}

resource "aws_api_gateway_deployment" "search_shoes_deployment" {
  rest_api_id = aws_api_gateway_rest_api.shoe_api.id
  depends_on = [
      aws_api_gateway_method.search_shoes_method,
      aws_api_gateway_integration.search_shoes_gateway
  ]
}

resource "aws_api_gateway_stage" "search_shoes_stage"{
  deployment_id = aws_api_gateway_deployment.search_shoes_deployment.id
  rest_api_id = aws_api_gateway_rest_api.shoe_api.id
  stage_name = "prod"
}

resource "aws_lambda_permission" "search_shoes_permissions"{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.search_shoes.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.shoe_api.execution_arn}/*/*"
  statement_id = "AllowAPIGatewayInvoke"
}

resource "aws_lambda_permission" "bedrock_invoke" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.search_shoes.function_name
  principal     = "bedrock.amazonaws.com"
  source_arn    = "arn:aws:bedrock:us-east-1:814929013775:agent/QTQ1JQCBEW"
  statement_id  = "AllowBedrockInvoke"
}

output "api_endpoint" {
  value = "${aws_api_gateway_stage.search_shoes_stage.invoke_url}/search"
}