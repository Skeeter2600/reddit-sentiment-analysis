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
    email = event["request"]["userAttributes"]["email"]
    print(email)

    try:
        table.put_item(
            Item={"email": email, "topics": []},
            ConditionExpression="attribute_not_exists(email)",
        )
    except Exception as e:
        print("User already exists in table.")

    return event
