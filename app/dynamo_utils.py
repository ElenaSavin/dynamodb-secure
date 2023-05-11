import boto3
import json
from botocore.exceptions import EndpointConnectionError

def connect_dynamodb(docker_registry_url, endpoint_url, region):
    try:
        client = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name=region)
    except Exception(EndpointConnectionError):
        return (json.dumps({"status": "Not Healthy!", "error": EndpointConnectionError, "container": docker_registry_url}))
    return client, json.dumps({"status": "Healthy!", "container": docker_registry_url})
    

def get_secret_code_from_dynamodb():
    return 1