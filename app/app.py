from flask import Flask, request, jsonify
import requests
from datetime import datetime
from dynamo_utils import get_secret_code_from_dynamodb, connect_dynamodb
import os

endpoint_url = os.environ["ENDPOINT_URL"]
region = os.environ["REGION"]

app = Flask(__name__)

@app.route('/health')
def health():
    docker_registry_url = "https://docker.registry.com/somepath"
    response = connect_dynamodb(docker_registry_url, endpoint_url, region)[1]
    return response

@app.route('/secret')
def secret():
    code_name = "thedoctor"
    secret_code = get_secret_code_from_dynamodb(code_name)
    response = {"codeName": code_name, "secretCode": secret_code}
    return jsonify(response)

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
    app.debug = True
    app.run(host="0.0.0.0")
    