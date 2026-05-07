# Importing LoginPage class
# used for UI login related operations
from pages.login_page import LoginPage

# Importing reusable API client
# used for API request handling
from api_client.api_client import APIClient


# NEGATIVE API TEST
# Validate API behavior for empty payload request
def test_empty_payload():
    
    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login("theepireddysathvika@gmail.com", "SathvikaReddy7")

    # Send create note request with empty payload
    res = api.create_note(token, {})

    # Validate API returns bad request status code
    assert res.status_code == 400