import boto3
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    client_s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='', region_name='us-east-1', endpoint_url='http://localhost:4572')
    client_s3.put_object(
        Bucket='Ledger',
        Key='b-key',
        Body='some body'
    )
    LOGGER.info("I've been called!")
    return {
        "event": str(event),
        "context": str(context.__dict__),
        "message": "Hello pytest!"
    }
