import os
import boto3

from common import TodoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    # delete the todo from the database
    table.delete_todo(event['pathParameters']['id'])

    # create a response
    response = {
        "statusCode": 200
    }

    return response
