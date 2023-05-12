import requests
import pytest
import json
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import app.dynamo_utils as dynamo

@pytest.fixture(scope='session')
def dynamodb():
    # Set up the DynamoDB connection for the test
    endpoint_url = 'http://localhost:8000'  # Example endpoint URL for a local DynamoDB instance
    region = 'eu-west-2'  # Example region
    docker_registry_url = 'http://example.com'  # Example Docker registry URL
    dynamodb, _ = dynamo.connect_dynamodb(docker_registry_url, endpoint_url, region)
    return dynamodb

#Verify the dynamodb status code
def test_status_code_dynamodb():
    status = requests.get("http://localhost:5000/health").status_code
    assert status == 200
    
@pytest.fixture(scope='session')
def test_get_secret_code_from_dynamodb(monkeypatch):
    # Define a mock response for DynamoDB's get_item method
    table_name = 'test_table'
    code_name = 'test_code'
    secret_code = 'some_secret_code'
    dynamodb = dynamodb()

    # Create the DynamoDB table for testing
    dynamo.create_dynamodb_table(table_name, dynamodb)

    # Insert the secret code into the table
    dynamo.insert_secret_into_dynamodb(dynamodb, secret_code, table_name, code_name)

    # Call the function being tested
    result = dynamo.get_secret_code_from_dynamodb(dynamodb, table_name, code_name)

    # Assertions
    expected_result = {'codeName': code_name, 'secretCode': secret_code}
    assert json.loads(result) == expected_result
