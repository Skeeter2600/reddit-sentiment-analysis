import json
import boto3
import os
from datetime import datetime

# DynamoDB init
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Posts")


def lambda_handler(event, context):
    if "queryStringParameters" in event and "topic" in event["queryStringParameters"]:
        topicParameter = event["queryStringParameters"]["topic"]
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'topic' paramter required"}),
        }

    posts = table.scan(
        FilterExpression="contains(Topics, :topic)",
        ExpressionAttributeValues={":topic": topicParameter},
    )["Items"]

    print(json.dumps(posts))

    return {"statusCode": 200, "body": json.dumps(posts)}
