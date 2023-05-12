import base64
import boto3
import json
from botocore.exceptions import ClientError
import logging
import sys

def connect_dynamodb(docker_registry_url, endpoint_url, region):
    """
    Connects to the DynamoDB service and returns a DynamoDB resource object.

    Args:
        docker_registry_url (str): The URL of the Docker registry.
        endpoint_url (str): The endpoint URL of the DynamoDB service.
        region (str): The AWS region where the DynamoDB service is located.

    Returns:
        dynamodb (boto3.resource): The DynamoDB resource object.
        response (str): JSON response indicating the connection status.

    """
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name=region)
    except Exception as e:
        logging.error(f"Not able to conect to dynamodb, ERROR: {e}")
        return None, (json.dumps({"status": "Not Healthy!", "error": str(e), "container": docker_registry_url}))
    logging.info("Connected to dynamo successfully")
    return dynamodb, json.dumps({"status": "Healthy!", "container": docker_registry_url})



def get_secret_code_from_dynamodb(dynamodb, table_name, code_name):
    """
    Retrieves the secret code from the specified DynamoDB table.

    Args:
        dynamodb (boto3.resource): The DynamoDB resource object.
        table_name (str): The name of the DynamoDB table.
        code_name (str): The code name to retrieve the secret code.

    Returns:
        str: JSON response containing the codeName and secretCode.

    """
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'codeName': code_name})
        secret_code = response['Item']['secretCode'].value
        return json.dumps({"codeName": code_name, "secretCode": secret_code.decode('utf-8')})
    except ClientError as e:
        logging.error(f"error retrieving secret: str({e})")
        return json.dumps({"error retrieving secret": str(e)})


def create_dynamodb_table(table_name, dynamodb):
    """
    Creates a DynamoDB table with the specified table name.

    Args:
        table_name (str): The name of the DynamoDB table.
        dynamodb (boto3.resource): The DynamoDB resource object.

    Returns:
        str: The name of the created table or the existing table.

    """
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
            logging.error(f"Table already exists")
            return table_name
        else:
            logging.error("Could not create table. This means the DynamoDB is not alive! Restart application!")
            return None


def insert_secret_into_dynamodb(dynamodb, secret_code, table_name, code_name):
    """
    Inserts the secret code into the specified DynamoDB table.

    Args:
        dynamodb (boto3.resource): The DynamoDB resource object.
        secret_code (bytes): The secret code to be inserted.
        table_name (str): The name of the DynamoDB table.
        code_name (str): The code name associated with the secret code.

    Returns:
        None

    """
    try:
        table = dynamodb.Table(table_name)

        # Insert the encrypted secret into DynamoDB
        table.put_item({'codeName': code_name, 'secretCode': secret_code})
        logging.info("mock secret inserted successfully")
    except ClientError as e:
            logging.error(json.dumps({"Error inserting secret into DynamoDB": str(e)}))

    def init(dynamodb, secret_code, table_name, code_name):
        """
        Initializes the application by creating the DynamoDB table and inserting the secret code.
        Args:
        dynamodb (boto3.resource): The DynamoDB resource object.
        secret_code (bytes): The secret code to be inserted.
        table_name (str): The name of the DynamoDB table.
        code_name (str): The code name associated with the secret code.

        Returns:
            None

        """
        try:
            create_dynamodb_table(table_name, dynamodb)
            insert_secret_into_dynamodb(dynamodb, secret_code, table_name, code_name)
        except Exception as e:
            logging.error(f"Encountered error {e}, shutting down")
            sys.exit()
        logging.info("Initiated successfully")