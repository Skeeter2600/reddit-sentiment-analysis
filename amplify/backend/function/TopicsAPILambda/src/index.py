import os
import json
import boto3


dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
table_name = os.environ["STORAGE_USERS_NAME"]
table = dynamodb.Table(table_name)

headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
}


def handler(event, context):
    method = event["httpMethod"]
    if method == "GET":
        response = get(event, context)
    elif method == "POST":
        response = post(event, context)
    elif method == "DELETE":
        response = delete(event, context)

    return response


def get(event, context):
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

    user = table.get_item(Key={"email": parameters["email"]})["Item"]
    print(user, user == None)

    if user == None:
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps([]),
        }

    topics = user["topics"]
    print(json.dumps(topics))

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(topics),
    }


def post(event, context):
    bad_parameters_response = {
        "statusCode": 400,
        "headers": headers,
        "body": json.dumps(
            {"Error": "Must specify the 'email', 'topic', and 'subreddit' parameters."}
        ),
    }

    parameters = {"email": None, "topic": None, "subreddit": None}

    if "queryStringParameters" not in event:
        return bad_parameters_response

    for param in parameters:
        if param not in event["queryStringParameters"]:
            return bad_parameters_response
        else:
            parameters[param] = event["queryStringParameters"][param]

    topic = {"topic": parameters["topic"], "subreddit": parameters["subreddit"]}

    try:
        table.update_item(
            Key={"email": parameters["email"]},
            ExpressionAttributeValues={":topic": topic, ":topics": [topic]},
            ConditionExpression="NOT contains(topics, :topic)",
            UpdateExpression="SET topics = list_append(topics, :topics)",
            ReturnValues="UPDATED_NEW",
        )
    except Exception as e:
        print(str(e))

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(event),
    }


def delete(event, context):
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(event),
    }
