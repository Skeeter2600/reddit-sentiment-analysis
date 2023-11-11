import json
import os
import boto3

# initialize AWS SDK clients
comprehend = boto3.client("comprehend")
dynamodb = boto3.resource("dynamodb")
table_name = "Posts"
env = os.environ["ENV"]
table = dynamodb.Table(f"{table_name}-{env}")


def handler(event, context):
    # loop through records provided by the DynamoDB Stream
    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            new_image = record["dynamodb"]["NewImage"]

            # retrieve relevant data from the new image
            post_id = new_image["postId"]["S"]
            post_title = new_image["title"]["S"]
            post_text = new_image["text"]["S"]

            full_text = f"{post_title}\n{post_text}"

            # check if it exceeds comprehend limit
            if len(full_text) > 5000:
                print("too big, analyzing only title")
                full_text = post_title

            # use Comprehend to perform sentiment analysis
            sentiment_response = comprehend.detect_sentiment(
                Text=full_text, LanguageCode="en"
            )
            sentiment = sentiment_response["Sentiment"]

            # write sentiment data back to DynamoDB
            table.update_item(
                Key={"postId": post_id},
                UpdateExpression="SET sentiment = :sentiment_val",
                ExpressionAttributeValues={":sentiment_val": sentiment},
                ReturnValues="UPDATED_NEW",
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('Hello from your new Amplify Python lambda!')
            }
