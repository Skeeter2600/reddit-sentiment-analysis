import os
import json
import boto3


headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
table_name = os.environ["STORAGE_USERS_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):
    method = event["httpMethod"]
    if method == "GET":
        response = get(event, context)
    elif method == "POST":
        response = post(event, context)

    return response


def get(event, context):
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(event),
    }


def post(event, context):
    bad_parameters_response = {
        "statusCode": 400,
        "headers": headers,
        "body": json.dumps({"Error": "Must specify the 'email' parameter."}),
    }

    parameters = {"email": None}

    if "queryStringParameters" not in event:
        return bad_parameters_response

    for param in parameters:
        if param not in event["queryStringParameters"]:
            return bad_parameters_response
        else:
            parameters[param] = event["queryStringParameters"][param]

    try:
        table.put_item(
            Item={"email": parameters["email"]},
            ConditionExpression="attribute_not_exists(email)",
        )
    except Exception as e:
        print("User already exists.")

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(event),
    }
