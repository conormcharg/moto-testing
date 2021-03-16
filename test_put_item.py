import unittest
import boto3 # AWS SDK for Python
from botocore.exceptions import ClientError
from moto import mock_dynamodb2
import os

@mock_dynamodb2
class TestPutItem(unittest.TestCase):
    def setUp(self):
        

        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
        TableName='TestDynamoDBTable',
        KeySchema=[
            {
                'AttributeName': 'Name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Location',
                'KeyType': 'RANGE'
            }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'Location',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    
    def tearDown(self):
        self.table.delete()
        self.dynamodb=None

    def test_put_item(self):
        from handler import put_item

        result = put_item("Conor", "Houston", self.dynamodb)
        self.assertEqual(200, result['statusCode'])
    
    def test_get_item(self):
        from handler import put_item
        from handler import get_item

        put_item("Conor", "Houston", self.dynamodb)
        result = get_item("Conor", "Houston", self.dynamodb)

        self.assertEqual("Houston", result['Location'])
        self.assertEqual("Conor", result['Name'])
        

if __name__ == '__main__':
    unittest.main()