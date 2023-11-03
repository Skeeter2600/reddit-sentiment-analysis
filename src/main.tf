provider "aws" {
  region = "us-east-1"
}

# policies

resource "aws_iam_policy" "cloudwatch_log_policy" {
  name    = "cloudwatch-log-policy"
  policy  = data.aws_iam_policy_document.cloudwatch_log_policy.json
}

resource "aws_iam_policy" "dynamodb_policy" {
  name    = "dynamodb-policy"
  policy  = data.aws_iam_policy_document.dynamodb_policy.json
}

resource "aws_iam_policy" "comprehend_policy" {
  name    = "comprehend-policy"
  policy  = data.aws_iam_policy_document.comprehend_policy.json
}

# roles and attachments

resource "aws_iam_role" "api_lambda_role" {
  name                = "api-lambda-execution-role"
  assume_role_policy  = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role" "comprehend_lambda_role" {
  name                = "comprehend-lambda-execution-role"
  assume_role_policy  = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_policy_attachment" "cloudwatch_log_policy_attachment" {
  name        = "cloudwatch-log-policy-attachment"
  policy_arn  = aws_iam_policy.cloudwatch_log_policy.arn

  roles = [
    aws_iam_role.api_lambda_role.name,
    aws_iam_role.comprehend_lambda_role.name
  ]
}

resource "aws_iam_policy_attachment" "dynamodb_policy_attachment" {
  name        = "dynamodb-policy-attachment"
  policy_arn  = aws_iam_policy.dynamodb_policy.arn

  roles = [
    aws_iam_role.api_lambda_role.name,
    aws_iam_role.comprehend_lambda_role.name
  ]
}

resource "aws_iam_policy_attachment" "comprehend_policy_attachment" {
  name        = "dynamodb-policy-attachment"
  policy_arn  = aws_iam_policy.comprehend_policy.arn

  roles = [
    aws_iam_role.comprehend_lambda_role.name
  ]
}

# /posts GET lambda integration

resource "aws_lambda_function" "posts_get_lambda" {
  filename      = "./lambdas/posts-get-lambda/lambda.zip"
  function_name = "posts-get-lambda"
  role          = aws_iam_role.api_lambda_role.arn
  handler       = "lambda.lambda_handler"
  runtime       = "python3.11"
}

# /posts POST lambda integration

resource "aws_lambda_function" "posts_post_lambda" {
  filename      = "./lambdas/posts-post-lambda/lambda.zip"
  function_name = "posts-post-lambda"
  role          = aws_iam_role.api_lambda_role.arn
  handler       = "lambda.lambda_handler"
  runtime       = "python3.11"

  environment {
    variables = {
      reddit_client_id = local.reddit_client_id
      reddit_client_secret = local.reddit_client_secret
    }
  }
}

# comprehend lambda

resource "aws_lambda_function" "comprehend_lambda" {
  filename      = "./lambdas/comprehend-lambda/lambda.zip"
  function_name = "comprehend-lambda"
  role          = aws_iam_role.comprehend_lambda_role.arn
  handler       = "lambda.lambda_handler"
  runtime       = "python3.11"
}

# the api gateway

resource "aws_api_gateway_rest_api" "reddit_api" {
  name        = "reddit-api-gateway"
  description = "API Gateway for the Reddit sentiment analysis app."
}

resource "aws_api_gateway_resource" "posts_resource" {
  rest_api_id = aws_api_gateway_rest_api.reddit_api.id
  parent_id   = aws_api_gateway_rest_api.reddit_api.root_resource_id
  path_part   = "posts"
}

# GET method

resource "aws_api_gateway_method" "posts_get_method" {
  rest_api_id   = aws_api_gateway_rest_api.reddit_api.id
  resource_id   = aws_api_gateway_resource.posts_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "posts_get_response_200" {
  rest_api_id     = aws_api_gateway_rest_api.reddit_api.id
  resource_id     = aws_api_gateway_resource.posts_resource.id
  http_method     = aws_api_gateway_method.posts_get_method.http_method
  status_code     = "200"
  response_models = {
    "application/json" = "Empty"
  }
}

# connect GET lambda to api

resource "aws_api_gateway_integration" "posts_get_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.reddit_api.id
  resource_id             = aws_api_gateway_resource.posts_resource.id
  http_method             = aws_api_gateway_method.posts_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.posts_get_lambda.invoke_arn
}

resource "aws_lambda_permission" "posts_get_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.posts_get_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn    = "${aws_api_gateway_deployment.reddit_api_deployment.execution_arn}/*"

  depends_on = [
    aws_api_gateway_deployment.reddit_api_deployment
  ]
}

# POST method

resource "aws_api_gateway_method" "posts_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.reddit_api.id
  resource_id   = aws_api_gateway_resource.posts_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "posts_post_response_200" {
  rest_api_id     = aws_api_gateway_rest_api.reddit_api.id
  resource_id     = aws_api_gateway_resource.posts_resource.id
  http_method     = aws_api_gateway_method.posts_post_method.http_method
  status_code     = "200"
  response_models = {
    "application/json" = "Empty"
  }
}

# connect POST lambda to api

resource "aws_api_gateway_integration" "posts_post_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.reddit_api.id
  resource_id             = aws_api_gateway_resource.posts_resource.id
  http_method             = aws_api_gateway_method.posts_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.posts_post_lambda.invoke_arn
}

resource "aws_lambda_permission" "api_gateway_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.posts_post_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn    = "${aws_api_gateway_deployment.reddit_api_deployment.execution_arn}/*"

  depends_on = [
    aws_api_gateway_deployment.reddit_api_deployment
  ]
}

# deploy the api

resource "aws_api_gateway_deployment" "reddit_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.reddit_api.id
  stage_name  = "prod"

  depends_on = [
    aws_api_gateway_integration.posts_get_lambda_integration,
    aws_api_gateway_integration.posts_post_lambda_integration
  ]
}

# dynamodb

resource "aws_dynamodb_table" "posts_table" {
  name              = "Posts"
  billing_mode      = "PROVISIONED"
  read_capacity     = 10
  write_capacity    = 10
  stream_enabled    = true
  stream_view_type  = "NEW_AND_OLD_IMAGES"
  hash_key          = "PostId"

  attribute {
    name = "PostId"
    type = "S"
  }
}

resource "aws_lambda_event_source_mapping" "comprehend_lambda_trigger" {
  event_source_arn  = aws_dynamodb_table.posts_table.stream_arn
  function_name     = aws_lambda_function.comprehend_lambda.arn
  starting_position = "LATEST"

  depends_on = [
    aws_dynamodb_table.posts_table,
    aws_lambda_function.comprehend_lambda
  ]
}