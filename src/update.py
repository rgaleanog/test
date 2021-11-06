import json
import logging
import os
import boto3

from utils import decimalencoder
from common import TodoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return

    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    result = table.update_todo(
                event['pathParameters']['id'], data['text'],
                data['checked']
            )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
