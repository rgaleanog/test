import json
import logging
import os

import boto3

from common import TodoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    result = table.put_todo(data['text'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response
