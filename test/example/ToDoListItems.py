import boto3
from botocore.exceptions import ClientError


def list_todo(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('todoTable')

    try:
        # fetch all todos from the database
        response = table.scan()

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


def main():
    todo = list_todo("")
    if todo:
        return todo


if __name__ == '__main__':
    main()
