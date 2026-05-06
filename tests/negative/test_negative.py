from pages.login_page import LoginPage
from api_client.api_client import APIClient


def test_empty_payload():
    
    api = APIClient()
    token = api.login("theepireddysathvika@gmail.com", "SathvikaReddy7")

    res = api.create_note(token, {})
    assert res.status_code == 400