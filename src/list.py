import json
import os
import boto3

from utils import decimalencoder
from common import TodoTableClass

if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')


def list(event, context):

    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    result = table.list_todo()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
