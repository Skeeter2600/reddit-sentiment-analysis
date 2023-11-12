import json

headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}


def handler(event, context):
    print("received event:")
    print(event)

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps("Hello from your new Amplify Python lambda!"),
    }
