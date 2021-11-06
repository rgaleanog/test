import os
import json
import boto3
from utils import decimalencoder
from common import TodoTableClass

if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource('dynamodb')

translate = boto3.client('translate')


def translate_function(text, source, target):

    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target
    )

    return response


def get(event, context):

    table = TodoTableClass.TodoTableClass(
                os.environ["DYNAMODB_TABLE"],
                dynamodb
            )

    result = table.get_todo(event['pathParameters']['id'])

    # translate text
    text = result['Item']['text']
    lang = event['pathParameters']['language']
    text = translate_function(text, "auto", lang)

    result['Item']['text'] = text['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
    }

    return response
