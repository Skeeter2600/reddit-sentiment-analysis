provider "aws" {
  region = "us-east-1"
}

resource "aws_amplify_app" "reddit_sentiment_analysis" {
  name       = "RedditSentimentApp"
  repository = "https://github.com/ssl3380/terraform-test"

  access_token = "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"

  iam_service_role_arn = aws_iam_role.amplify_service_role.arn

  build_spec = <<-EOT
    version: 0.1
    frontend:
      phases:
        preBuild:
          commands:
            - npm install
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: dist
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
    backend:
      phases:
        preBuild:
          commands:
            - ln -fs /usr/local/bin/pip3.8 /usr/bin/pip3
            - ln -fs /usr/local/bin/python3.8 /usr/bin/python3
            - pip3 install --user pipenv
        build:
          commands:
            - amplifyPush --simple
  EOT

  environment_variables = {
    ENV = "test"
  }
}

resource "aws_amplify_branch" "amplify_branch" {
  app_id      = aws_amplify_app.reddit_sentiment_analysis.id
  branch_name = "main"
  enable_auto_build = true
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
        type = "Service"
        identifiers = ["amplify.us-east-1.amazonaws.com", "amplify.amazonaws.com"]
    }
  }
}

data "aws_iam_policy" "administrator_access_amplify" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess-Amplify"
}

resource "aws_iam_role" "amplify_service_role" {
  name                = "amplify-service-role"
  assume_role_policy  = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "amplify_service_role_attachment" {
  role       = aws_iam_role.amplify_service_role.name
  policy_arn = data.aws_iam_policy.administrator_access_amplify.arn
}

resource "aws_amplify_webhook" "main" {
  app_id      = aws_amplify_app.reddit_sentiment_analysis.id
  branch_name = aws_amplify_branch.amplify_branch.branch_name
  description = "triggermaster"
}

output "triggerurl" {
  value = aws_amplify_webhook.main.url
}