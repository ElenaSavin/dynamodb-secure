import unittest
from unittest.mock import MagicMock
from app import connect_dynamodb, get_secret_code_from_dynamodb

class DynamoDBTestCase(unittest.TestCase):
    def setUp(self):
        self.dynamodb = MagicMock()
        self.docker_registry_url = 'https://my-docker-registry.com'
        self.endpoint_url = 'https://my-dynamodb-endpoint.com'
        self.region = 'us-west-2'
        self.table_name = 'my_table'
        self.code_name = 'my_code'

    def test_connect_dynamodb_successful(self):
        self.dynamodb.resource.return_value = self.dynamodb

        dynamodb, response = connect_dynamodb(
            self.docker_registry_url, self.endpoint_url, self.region
        )

        self.assertEqual(dynamodb, self.dynamodb)
        self.assertEqual(
            response,
            {
                'status': 'Healthy!',
                'container': self.docker_registry_url
            }
        )

    def test_connect_dynamodb_failure(self):
        self.dynamodb.resource.side_effect = Exception('Connection Error')

        dynamodb, response = connect_dynamodb(
            self.docker_registry_url, self.endpoint_url, self.region
        )

        self.assertIsNone(dynamodb)
        self.assertEqual(
            response,
            {
                'status': 'Not Healthy!',
                'error': 'Connection Error',
                'container': self.docker_registry_url
            }
        )

    def test_get_secret_code_from_dynamodb_successful(self):
        table = MagicMock()
        response_item = {'codeName': self.code_name, 'secretCode': 'my_secret_code'}
        table.get_item.return_value = {'Item': response_item}
        self.dynamodb.Table.return_value = table

        secret_code = get_secret_code_from_dynamodb(
            self.dynamodb, self.table_name, self.code_name
        )

        expected_response = {
            'codeName': self.code_name,
            'secretCode': response_item['secretCode']
        }
        self.assertEqual(secret_code, expected_response)

    def test_get_secret_code_from_dynamodb_failure(self):
        table = MagicMock()
        table.get_item.side_effect = ClientError(
            {'Error': {'Code': 'ValidationException', 'Message': 'Item not found'}},
            'GetItem'
        )
        self.dynamodb.Table.return_value = table

        response = get_secret_code_from_dynamodb(
            self.dynamodb, self.table_name, self.code_name
        )

        expected_response = {'error retrieving secret': 'An error occurred'}
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()
