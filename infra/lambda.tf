data "archive_file" "search_shoes" {
  type = "zip"
  source_file = "../lambda/search_shoes/lambda_function.py"
  output_path = "../lambda/search_shoes/lambda_function.zip"
}

resource "aws_lambda_function" "search_shoes" {
  filename      =  data.archive_file.search_shoes.output_path
  function_name = "search_shoes"
  role          = aws_iam_role.database_read_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  source_code_hash = data.archive_file.search_shoes.output_base64sha256
}

# Allow Bedrock to invoke the search_shoes Lambda
resource "aws_lambda_permission" "bedrock_invoke" {
  statement_id  = "AllowBedrockInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.search_shoes.function_name
  principal     = "bedrock.amazonaws.com"
  source_arn    = "arn:aws:bedrock:${var.aws_region}:814929013775:agent/${var.bedrock_agent_id}"
}
