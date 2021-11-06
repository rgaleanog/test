import boto3


def create_todo_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url='http://localhost:8000')

    table = dynamodb.create_table(
        TableName='todoTable',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='todoTable')
    if (table.table_status != 'ACTIVE'):
        raise AssertionError()

    return table


if __name__ == '__main__':
    print("Table status:", create_todo_table().table_status)
