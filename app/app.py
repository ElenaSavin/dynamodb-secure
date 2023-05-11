from flask import Flask, request, jsonify
import requests
from datetime import datetime
from dynamo_utils import get_secret_code_from_dynamodb, connect_dynamodb
import os

endpoint_url = os.environ["ENDPOINT_URL"]
region = os.environ["REGION"]
docker_registry_url = os.environ["REGISTRY"]

app = Flask(__name__)

dynamodb, response = connect_dynamodb(docker_registry_url, endpoint_url, region)

@app.route('/health')
def health(response):
    return response

@app.route('/secret')
def secret(dynamodb):
    try:
        code_name = os.environ["CODENAME"]
        secret_code = get_secret_code_from_dynamodb(dynamodb, code_name)
        response = {"codeName": code_name, "secretCode": secret_code}
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": e})

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
    