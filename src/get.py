import os
import json
import boto3

from utils import decimalencoder
from common import TodoTableClass

if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')


def get(event, context):

    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    result = table.get_todo(event['pathParameters']['id'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
    }

    return response
