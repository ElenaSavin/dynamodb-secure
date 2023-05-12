import base64
import boto3
import json
from botocore.exceptions import ClientError
import logging
import sys

def connect_dynamodb(docker_registry_url, endpoint_url, region):
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name=region)
    except Exception as e:
        return None, (json.dumps({"status": "Not Healthy!", "error": str(e), "container": docker_registry_url}))
    return dynamodb, json.dumps({"status": "Healthy!", "container": docker_registry_url})
    

def get_secret_code_from_dynamodb(dynamodb, table_name, code_name):
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'codeName': code_name})
        secret_code = response['Item']['secretCode'].value
        return json.dumps({"codeName": code_name, "secretCode": secret_code.decode('utf-8')})
    except ClientError as e:
        return json.dumps({"error retrieving secret": str(e)})

def create_dynamodb_table(table_name, dynamodb):
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'codeName',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'codeName',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        return table_name

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            return table_name
        else:
            print("Could not create table. this means the dynamodb is not alive!!! restart application!")
            return None
            
def insert_secret_into_dynamodb(dynamodb, secret_code, table_name, code_name):
    try:
        table = dynamodb.Table(table_name)

        # Insert the encrypted secret into DynamoDB
        table.put_item(Item={'codeName': code_name, 'secretCode': secret_code})
        print(json.dumps({"status": "Secret inserted successfully."}))

    except ClientError as e:
        print(json.dumps({"Error inserting secret into DynamoDB": str(e)}))

def init(dynamodb, secret_code, table_name, code_name):
    try:
        create_dynamodb_table(table_name, dynamodb)
        insert_secret_into_dynamodb(dynamodb, secret_code, table_name, code_name)
    except Exception as e:
        print(f"Encountered error {e}, shutting down")
        sys.exit()

