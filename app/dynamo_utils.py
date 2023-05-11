import boto3
import json

def connect_dynamodb(docker_registry_url, endpoint_url, region):
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name=region)
    except Exception as e:
        return None, (json.dumps({"status": "Not Healthy!", "error": e, "container": docker_registry_url}))
    return dynamodb, json.dumps({"status": "Healthy!", "container": docker_registry_url})
    

def get_secret_code_from_dynamodb(dynamodb, code_name):
    table = dynamodb.Table('devops-challenge')
    response = table.get_item(Key={'codeName': code_name})
    secret_code = response['Item']['secretCode']
    return secret_code
