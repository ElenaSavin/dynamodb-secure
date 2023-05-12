from flask import Flask, request, jsonify
import requests
from datetime import datetime
from dynamo_utils import init, get_secret_code_from_dynamodb, connect_dynamodb
import os
import secrets
import string
import base64

alphabet = string.ascii_letters + string.digits

password = ''.join(secrets.choice(alphabet) for i in range(20))
print(password)
secret_code=base64.b64encode(password.encode("utf-8"))  


endpoint_url = os.environ["ENDPOINT_URL"]
region = os.environ["REGION"]
docker_registry_url = os.environ["REGISTRY"]
code_name = os.environ["CODE_NAME"]
table_name = os.environ["TABLE_NAME"]

app = Flask(__name__)

dynamodb, response = connect_dynamodb(docker_registry_url, endpoint_url, region)

@app.route('/health')
def health():
    return response

@app.route('/secret')
def secret():
    return get_secret_code_from_dynamodb(dynamodb, table_name, code_name)

@app.errorhandler(404)
def page_not_found(e):
    """Handling page not found error - 
    will always display this text instead of the browser usual error

    Args:
        e error

    Returns:
        string: page not found
    """
    return "404 Page not found"

if __name__ == '__main__':
    init(dynamodb, secret_code, table_name, code_name)
    app.debug = True
    app.run(host="0.0.0.0")
    