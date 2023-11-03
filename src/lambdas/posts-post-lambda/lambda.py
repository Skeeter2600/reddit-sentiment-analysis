import json
import boto3
import praw
import os
from datetime import datetime

# reddit API config
reddit = praw.Reddit(
    client_id=os.environ["reddit_client_id"],
    client_secret=os.environ["reddit_client_secret"],
    user_agent="dev",
)

# DynamoDB init
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Posts")


# upload data to dynamoDB
def upload_to_dynamodb(post, topic):
    try:
        data = {
            "PostId": post.id,
            "Subreddit": post.subreddit.display_name,
            "Title": post.title,
            "Text": post.selftext,
            "Datetime": format_date(post.created_utc),
            "Topics": [topic],
        }

        table.put_item(Item=data, ConditionExpression="attribute_not_exists(PostId)")
    except Exception as existsException:
        try:
            table.update_item(
                Key={"PostId": post.id},
                UpdateExpression="SET Topics = list_append(Topics, :topics)",
                ConditionExpression="NOT contains(Topics, :topic)",
                ExpressionAttributeValues={":topics": [topic], ":topic": topic},
                ReturnValues="UPDATED_NEW",
            )
        except Exception as inListException:
            print(str(inListException))


# format date, convert timestamp to a string in the format 'YYYY-MM-DD HH:MM:SS'
def format_date(time):
    dt = datetime.fromtimestamp(time)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def lambda_handler(event, context):
    if "queryStringParameters" in event and "limit" in event["queryStringParameters"]:
        limitParameter = event["queryStringParameters"]["limit"]
    else:
        limitParameter = "10"

    if (
        "queryStringParameters" in event
        and "subreddit" in event["queryStringParameters"]
    ):
        subredditParameter = event["queryStringParameters"]["subreddit"]
    else:
        subredditParameter = "all"

    if "queryStringParameters" in event and "topic" in event["queryStringParameters"]:
        topicParameter = event["queryStringParameters"]["topic"]
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'topic' paramter required"}),
        }

    try:
        limit = int(limitParameter)
    except Exception as e:
        print(str(e))
    subreddit = reddit.subreddit(subredditParameter)

    posts = subreddit.search(query=topicParameter, sort="hot", limit=limit)

    for post in posts:
        upload_to_dynamodb(post, topicParameter)

    return {"statusCode": 200, "body": json.dumps("success")}
