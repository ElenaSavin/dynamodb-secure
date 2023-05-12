import unittest
from flask import Flask
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Healthy', response.data)

    def test_secret_endpoint(self):
        response = self.client.get('/secret')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'codeName', response.data)
        self.assertIn(b'secretCode', response.data)

    def test_invalid_endpoint(self):
        response = self.client.get('/invalid')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Page not found', response.data)

if __name__ == '__main__':
    unittest.main()
