import boto3
import logging
import os


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def make_s3():
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    region_name = os.environ['AWS_REGION']
    s3_endpoint_url = os.environ['S3_ENDPOINT_URL']
    return boto3.client('s3', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name,
                        endpoint_url=s3_endpoint_url)


def handler(event, context):
    LOGGER.info('event: {}'.format(str(event)))
    LOGGER.info('context: {}'.format(str(context)))


    #bucket_name = os.environ['BUCKET_NAME']
    #client_s3 = make_s3()
    #client_s3.put_object(
    #    Bucket=bucket_name,
    #    Key='b-key',
    #    Body='some body'
    #)

    LOGGER.info("I've been called!")
    return {
        "event": str(event),
        "context": str(context.__dict__),
        "message": "Hello TEST!"
    }
