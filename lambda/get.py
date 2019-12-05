import os
import json
import logging
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def get(event, context):
    LOGGER.info('modules: ' + str(dir()))
    import decimalencoder
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response