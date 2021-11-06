import boto3
import time
import uuid
from botocore.exceptions import ClientError


class TodoTableClass(object):
    def __init__(self, table, dynamodb=None):

        self.tableName = table
        # Dynamodb conection
        if not dynamodb:
            dynamodb = boto3.resource(
                            "dynamodb",
                            endpoint_url="http://dynamodb:8000"
                        )

        self.dynamodb = dynamodb

    # Create table in Dynamodb
    def create_todo_table(self):

        try:
            table = self.dynamodb.create_table(
                TableName=self.tableName,
                KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(
                TableName=self.tableName
            )

            if (table.table_status != 'ACTIVE'):
                raise AssertionError()
        except ClientError as e:
            print("Create Error: " + e.response["Error"]["Message"])
        else:
            # print("Create OK: " + self.tableName )
            return table

    # Create item in Dynamodb
    def put_todo(self, text, id=None):

        if not id:
            id = str(uuid.uuid1())

        timestamp = str(time.time())
        table = self.dynamodb.Table(self.tableName)

        try:
            item = {
                "id": id,
                "text": text,
                "checked": False,
                "createAt": timestamp,
                "updateAt": timestamp
            }

            table.put_item(Item=item)
            response = item

        except ClientError as e:
            print("Insert Error: " + e.response["Error"]["Message"])
        else:
            # print("Insert OK - id:" + item["id"] + " text: " + item["text"] )
            return response

    # Get item from Dynamodb
    def get_todo(self, id):

        table = self.dynamodb.Table(self.tableName)
        try:
            response = table.get_item(Key={"id": id})
        except ClientError as e:
            print("GET Error: " + e.response["Error"]["Message"])
        else:
            return response

    # List items from Dynamodb
    def list_todo(self):

        table = self.dynamodb.Table(self.tableName)

        try:
            response = table.scan()
        except ClientError as e:
            print("List Error: " + e.response["Error"]["Message"])
        else:
            return response

    # Update item in Dynamodb
    def update_todo(self, id, text, checked):

        table = self.dynamodb.Table(self.tableName)
        timestamp = str(time.time())

        try:
            response = table.update_item(
                Key={
                    'id': id
                },
                ExpressionAttributeNames={
                    '#todo_text': 'text',
                },
                ExpressionAttributeValues={
                  ':text': text,
                  ':checked': checked,
                  ':updatedAt': timestamp
                },
                UpdateExpression='SET #todo_text = :text, '
                                 'checked = :checked, '
                                 'updatedAt = :updatedAt',
                ReturnValues='ALL_NEW'
            )
        except ClientError as e:
            print("Update Error: " + e.response["Error"]["Message"])
        else:
            return response

    # Delete item from Dynamodb
    def delete_todo(self, id):

        table = self.dynamodb.Table(self.tableName)
        try:
            response = table.delete_item(Key={"id": id})
        except ClientError as e:
            print("Delete Error: " + e.response["Error"]["Message"])
        else:
            return response
