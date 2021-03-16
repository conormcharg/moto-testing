import json
import boto3
from botocore.exceptions import ClientError
import os

#TEST_TABLE = os.environ['TEST_TABLE']

def add_entry(event, context):

    dynamodb = boto3.resource('dynamodb')


    if event["httpMethod"] == "POST" and event["body"]:
        print(event)
        received = json.loads(event["body"])
        name = received["name"]
        location = received["location"]

        response = put_item(name, location, dynamodb)

        r = {
            'statusCode': 200,
            'body': event
        }

        return r

    response= {
            "statusCode":200
        }

    return response


def put_item(name, location, dynamodb):
    tableName = dynamodb.Table('TestDynamoDBTable')

    try:
        tableName.put_item(
            Item={
                'Name':name,
                'Location':location
            }
        )

        return {
            'statusCode': 200,
            'body':json.dumps('Success!')
        }
    except:
        print('Closing Lambda function')
        return{
            'statusCode': 400,
            'body':json.dumps('Error Saving temp!')
        }


def get_item(name, location, dynamodb):

    table = dynamodb.Table('TestDynamoDBTable')
    try:
        response = table.get_item(Key={'Name': name, 'Location': location})
        return response['Item']
    except ClientError as e:
        print(e.response['Error']['Message'])

    
