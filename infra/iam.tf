resource "aws_iam_role" "database_read_role"{
  name = "database_read_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    =  ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }]
  })
}

resource "aws_iam_policy" "database_read_policy"{
  name = "database_read_policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Effect = "Allow",
        Resource = aws_dynamodb_table.shoe-inventory-table.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "database_read_attach"{
  role = aws_iam_role.database_read_role.name
  policy_arn = aws_iam_policy.database_read_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.database_read_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Bedrock Agent IAM Role
resource "aws_iam_role" "bedrock_agent_role" {
  name = "bedrock_agent_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = "814929013775"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "bedrock_agent_policy" {
  name = "bedrock_agent_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "lambda:InvokeFunction"
        Resource = aws_lambda_function.search_shoes.arn
      },
      {
        Effect   = "Allow"
        Action   = "bedrock:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_agent_attach" {
  role       = aws_iam_role.bedrock_agent_role.name
  policy_arn = aws_iam_policy.bedrock_agent_policy.arn
}

output "bedrock_agent_role_arn" {
  value = aws_iam_role.bedrock_agent_role.arn
}