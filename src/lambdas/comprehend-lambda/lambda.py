import json
import boto3

# initialize AWS SDK clients
comprehend = boto3.client("comprehend")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Posts")


def lambda_handler(event, context):
    # loop through records provided by the DynamoDB Stream
    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            new_image = record["dynamodb"]["NewImage"]

            # retrieve relevant data from the new image
            post_id = new_image["PostId"]["S"]
            post_title = new_image["Title"]["S"]
            post_text = new_image["Text"]["S"]

            full_text = f"{post_title}\n{post_text}"

            # check if it exceeds comprehend limit
            if len(full_text) > 5000:
                full_text = full_text[0:5000]

            # use Comprehend to perform sentiment analysis
            sentiment_response = comprehend.detect_sentiment(
                Text=full_text, LanguageCode="en"
            )
            sentiment = sentiment_response["Sentiment"]

            # write sentiment data back to DynamoDB
            table.update_item(
                Key={"PostId": post_id},
                UpdateExpression="SET Sentiment = :sentiment_val",
                ExpressionAttributeValues={":sentiment_val": sentiment},
                ReturnValues="UPDATED_NEW",
            )
