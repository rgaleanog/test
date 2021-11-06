# from pprint import pprint
import warnings
import unittest
import boto3
import time
import uuid

from moto import mock_dynamodb2
import sys

sys.path.insert(0, '../../src/common')
from TodoTableClass import TodoTableClass

table_doker = "TodoTableDocker"
table_aws = "TodoTable"

@mock_dynamodb2
class TestToDoTableClass(unittest.TestCase):


    def setUp(self):
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")

        """Create the mock database and table"""
        self.dynamodb_aws = boto3.resource('dynamodb', region_name='us-east-1')
        self.dynamodb_docker = boto3.resource("dynamodb", endpoint_url="http://localhost:8000", region_name='us-east-1')

        self.uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.text = "Aprender DevOps y Cloud en la UNIR"

        self.table_handler_docker = TodoTableClass(table_doker, self.dynamodb_docker)
        self.table_docker = self.table_handler_docker.create_todo_table()

        self.table_handler_aws = TodoTableClass(table_aws, self.dynamodb_aws)
        self.table_aws = self.table_handler_aws.create_todo_table()

    def tearDown(self):
        """Delete mock database and table after test is run"""
        self.table_docker.delete()
        self.table_aws.delete()

        self.dynamodb_aws = None
        self.dynamodb_docker = None

    def test_table_exists(self):
        self.assertTrue(self.table_docker)  # check if we got a result
        self.assertTrue(self.table_aws)  # check if we got a result

        # check if the table name is 'ToDo'
        self.assertIn(table_doker, self.table_docker.name)
        self.assertIn(table_aws, self.table_aws.name)


    def test_put_todo(self):

        # Table local
        self.assertEqual(self.uuid, self.table_handler_docker.put_todo(self.text, self.uuid)['id'])

        # Table mock
        self.assertEqual(self.uuid, self.table_handler_aws.put_todo(self.text, self.uuid)['id'])

    def test_put_todo_error(self):

        # Table local
        self.assertRaises(Exception, self.table_handler_docker.put_todo("", self.uuid))
        self.assertRaises(Exception, self.table_handler_docker.put_todo("", ""))
        self.assertRaises(Exception, self.table_handler_docker.put_todo(self.text, ""))

        # Table mock
        self.assertRaises(Exception, self.table_handler_aws.put_todo("", self.uuid))
        self.assertRaises(Exception, self.table_handler_aws.put_todo("", ""))
        self.assertRaises(Exception, self.table_handler_aws.put_todo(self.text, ""))

    def test_get_todo(self):

        # Table local
        self.table_handler_docker.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_docker.get_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])
        self.assertEqual(self.text, self.table_handler_docker.get_todo(self.uuid)['Item']['text'])

        # Table mock
        self.table_handler_aws.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_aws.get_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])
        self.assertEqual(self.text, self.table_handler_aws.get_todo(self.uuid)['Item']['text'])


    def test_list_todo(self):

        # Table local
        self.table_handler_docker.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_docker.list_todo()['ResponseMetadata']['HTTPStatusCode'])

        # Table mock
        self.table_handler_aws.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_aws.list_todo()['ResponseMetadata']['HTTPStatusCode'])

    def test_update_todo(self):

        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"

        # Table local
        self.table_handler_docker.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_docker.update_todo(self.uuid, updated_text, "false")['ResponseMetadata']['HTTPStatusCode'])
        self.assertEqual(updated_text, self.table_handler_docker.get_todo(self.uuid)['Item']['text'])

        # Table mock
        self.table_handler_aws.put_todo(self.text, self.uuid)
        self.assertEqual(
            200,
            self.table_handler_aws.update_todo(
                self.uuid,
                updated_text,
                "false"
            )['ResponseMetadata']['HTTPStatusCode'])
        self.assertEqual(
            updated_text,
            self.table_handler_aws.get_todo(
                self.uuid
            )['Item']['text'])

    def test_update_todo_error(self):

        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"

        # Table local
        self.table_handler_docker.put_todo(self.text, self.uuid)
        self.assertRaises(Exception, self.table_handler_docker.update_todo("", updated_text,  "false"))
        self.assertRaises(TypeError, self.table_handler_docker.update_todo(self.uuid, "",  "false"))
        self.assertRaises(Exception, self.table_handler_docker.update_todo(self.uuid, updated_text, ""))

        # Table mock
        self.table_handler_aws.put_todo(self.text, self.uuid)
        self.assertRaises(
            Exception,
            self.table_handler_aws.update_todo(
                "",
                updated_text,
                "false"
            ))

        self.assertRaises(
            TypeError,
            self.table_handler_aws.update_todo(
                self.uuid,
                "",
                "false"
            ))

        self.assertRaises(
            Exception,
            self.table_handler_aws.update_todo(
                self.uuid,
                updated_text,
                ""
            ))

    def test_delete_todo(self):

        # Table local
        self.table_handler_docker.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_docker.delete_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])

        # Table mock
        self.table_handler_aws.put_todo(self.text, self.uuid)
        self.assertEqual(200, self.table_handler_aws.delete_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])

    def test_delete_todo_error(self):

        # Table local
        self.assertRaises(TypeError, self.table_handler_docker.delete_todo(""))
        self.assertRaises(TypeError, self.table_handler_docker.delete_todo(""))

        # Table mock
        self.assertRaises(TypeError, self.table_handler_aws.delete_todo(""))

if __name__ == '__main__':
    unittest.main()
