import json
import os
import logging
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def list(event, context):
    LOGGER.info('modules: ' + str(dir()))
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
