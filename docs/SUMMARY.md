# Application Overview

This application is a simple Flask web server that interacts with an AWS DynamoDB database to store and retrieve a secret code. It is designed to run within a containerized environment (e.g., Docker).

Notes:
- Assumed that the login to Dynamodb is authanticated with aws sso/access keys. here are set dummy entries
- Asumed some encryption is set on the secrets such like KMS. Just for example base64 was used.

## Setup and Dependencies

This application requires the following environment variables to be set:

- `ENDPOINT_URL`: The endpoint URL of the DynamoDB service.
- `REGION`: The AWS region where the DynamoDB service is located.
- `REGISTRY`: The URL of the Docker registry.
- `CODE_NAME`: The code name associated with the secret code.
- `TABLE_NAME`: The name of the DynamoDB table.

The Python dependencies include:

- Flask
- boto3
- requests
- datetime
- os
- secrets
- string
- base64
- logging

* Note - requires docker and docker-compose
## How to Run

docker-compose up --build


## How to Test

In the test directory run pytest. 
These are example test for the router and application.

The Python dependencies include:

- requests
- pytest

## Application Endpoints
  
This application has two main endpoints:

1. `/health`: This endpoint returns the health status of the application and the Docker container information. This is useful for monitoring and debugging purposes.

2. `/secret`: This endpoint retrieves the secret code from the DynamoDB table and returns it in the JSON response.

A custom 404 error handler is also implemented to return a message when a page is not found.

## DynamoDB Interaction

This application uses the boto3 AWS SDK to interact with DynamoDB. It includes the following main DynamoDB operations:

- Connect to DynamoDB service
- Create a DynamoDB table if it doesn't exist
- Insert the secret code into the DynamoDB table
- Retrieve the secret code from the DynamoDB table

The DynamoDB table uses `codeName` as the primary key (hash key). The secret code is stored in the `secretCode` attribute of the DynamoDB items. All the DynamoDB-related operations are encapsulated in the `dynamo_utils.py` script.


This application uses Python's built-in logging module to log important events and errors. The log level is set to `ERROR`showing in stdout.