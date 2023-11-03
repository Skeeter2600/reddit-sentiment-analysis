output "api_url" {
  value         = aws_api_gateway_deployment.reddit_api_deployment.invoke_url
  description   = "url used to invoke the api"
}