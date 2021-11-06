import boto3
from botocore.exceptions import ClientError


def delete_todo(id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('todoTable')

    try:
        # delete the todo from the database
        response = table.delete_item(
            Key={
                'id': id
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


def main():
    todo = delete_todo("123e4567-e89b-12d3-a456-426614174000")
    if todo:
        return todo


if __name__ == '__main__':
    main()
