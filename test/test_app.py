import requests
import pytest

# Verify code 404 response when approaching non existing path
def test_page_not_found_response():
    response = requests.get("http://localhost:5000/secre").text
    assert response == "404 Page not found"

# Verify status code is 200 when reaching secret api
def test_status_code_create_response():
    status = requests.get("http://localhost:5000/secret").status_code
    assert status == 200

# Verify API response time is not to long
def test_verify_secret_api_response_time():
    response_time = requests.get("http://localhost:5000/secret").elapsed.total_seconds()
    if response_time < 1:
        return "Success! response time under 1 second"
    return f"Oh No! response took too long {response_time}"

# Verify content-type header and response body secret api
def test_verify_content_type_header():
    header = requests.get("http://localhost:5000/secret").headers
    assert header["Content-Type"] == "application/json"
