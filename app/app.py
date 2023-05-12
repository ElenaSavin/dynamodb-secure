from flask import Flask, request, jsonify
import requests
from datetime import datetime
from dynamo_utils import init, get_secret_code_from_dynamodb, connect_dynamodb
import os
import secrets
import string
import base64

# Set variables
alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for _ in range(20))
secret_code = base64.b64encode(password.encode("utf-8"))
endpoint_url = os.environ["ENDPOINT_URL"]
region = os.environ["REGION"]
docker_registry_url = os.environ["REGISTRY"]
code_name = os.environ["CODE_NAME"]
table_name = os.environ["TABLE_NAME"]

app = Flask(__name__)

# Connect to DynamoDB
dynamodb, response = connect_dynamodb(docker_registry_url, endpoint_url, region)

@app.route('/health')
def health():
    """
    Health endpoint that returns the health status and container information.

    Returns:
        str: JSON response with health status and container information
    """
    return response

@app.route('/secret')
def secret():
    """
    Secret endpoint that retrieves the secret code from DynamoDB.

    Returns:
        str: JSON response with the secret code
    """
    return get_secret_code_from_dynamodb(dynamodb, table_name, code_name)

@app.errorhandler(404)
def page_not_found(e):
    """
    Error handler for 404 page not found.

    Args:
        e (Exception): The error object

    Returns:
        str: Custom 404 page not found message
    """
    return "404 Page not found"

if __name__ == '__main__':
    # Initialize DynamoDB table and insert the secret code
    init(dynamodb, secret_code, table_name, code_name)

    app.debug = True
    app.run(host="0.0.0.0")
