import boto3
import logging
import os


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def make_s3():
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    REGION_NAME = os.environ['AWS_REGION']
    S3_ENDPOINT_URL = os.environ['S3_ENDPOINT_URL']
    return boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=REGION_NAME,
                        endpoint_url=S3_ENDPOINT_URL)


def handler(event, context):
    BUCKET_NAME = os.environ['BUCKET_NAME']
    client_s3 = make_s3()
    client_s3.put_object(
        Bucket=BUCKET_NAME,
        Key='b-key',
        Body='some body 2234'
    )
    LOGGER.info("I've been called!")
    return {
        "event": str(event),
        "context": str(context.__dict__),
        "message": "Hello TEST 1222!"
    }
