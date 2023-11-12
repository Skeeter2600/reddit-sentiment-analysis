import json
import boto3
import praw
import os

headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

# reddit API config
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="dev",
)

# DynamoDB init
dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
table_name = os.environ["STORAGE_POSTS_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):
    method = event["httpMethod"]
    if method == "GET":
        response = get(event, context)
    elif method == "POST":
        response = post(event, context)

    return response


def get(event, context):
    bad_parameters_response = {
        "statusCode": 400,
        "headers": headers,
        "body": json.dumps(
            {
                "error": "must specify 'topic', 'subreddit', and 'limit' parameters. limit must be an integer."
            }
        ),
    }

    if "queryStringParameters" not in event:
        return bad_parameters_response

    parameters = {"topic": None, "subreddit": None}

    for param in parameters:
        if param not in event["queryStringParameters"]:
            return bad_parameters_response
        else:
            parameters[param] = event["queryStringParameters"][param]

    posts = table.scan(
        FilterExpression="contains(topics, :topic) and subreddit = :subreddit",
        ExpressionAttributeValues={
            ":topic": parameters["topic"],
            ":subreddit": parameters["subreddit"],
        },
    )["Items"]

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(posts),
    }


def post(event, context):
    bad_parameters_response = {
        "statusCode": 400,
        "headers": headers,
        "body": json.dumps(
            {
                "error": "must specify 'topic', 'subreddit', and 'limit' parameters. limit must be an integer."
            }
        ),
    }

    if "queryStringParameters" not in event:
        return bad_parameters_response

    parameters = {"topic": None, "subreddit": None, "limit": None}

    for param in parameters:
        if param not in event["queryStringParameters"]:
            return bad_parameters_response
        else:
            parameters[param] = event["queryStringParameters"][param]

    try:
        str(parameters["topic"])
        str(parameters["subreddit"])
        int(parameters["limit"])
    except Exception as e:
        print(str(e))
        return bad_parameters_response

    subreddit = reddit.subreddit(parameters["subreddit"])

    posts = subreddit.search(
        query=parameters["topic"], sort="new", limit=int(parameters["limit"])
    )

    for post in posts:
        upload_to_dynamodb(post, parameters["topic"])

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(event),
    }


# upload data to dynamoDB
def upload_to_dynamodb(post, topic):
    try:
        data = {
            "postId": post.id,
            "subreddit": post.subreddit.display_name,
            "topics": [topic],
            "title": post.title,
            "text": post.selftext,
        }

        table.put_item(Item=data, ConditionExpression="attribute_not_exists(postId)")
    except Exception as existsException:
        try:
            table.update_item(
                Key={"postId": post.id},
                UpdateExpression="SET Topics = list_append(topics, :topics)",
                ConditionExpression="NOT contains(topics, :topic)",
                ExpressionAttributeValues={":topics": [topic], ":topic": topic},
                ReturnValues="UPDATED_NEW",
            )
        except Exception as inListException:
            print(str(inListException))
