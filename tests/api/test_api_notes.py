from api_client.api_client import APIClient
import time

# 🔐 Credentials
EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


def test_get_notes():
    api = APIClient()
    token = api.login(EMAIL, PASS)

    res = api.get_notes(token)

    assert res.status_code == 200
    assert res.elapsed.total_seconds() < 5

    data = res.json()
    assert "data" in data


def test_create_note():
    api = APIClient()
    token = api.login(EMAIL, PASS)

    payload = {
        "title": "Test Note Title",   # ✅ > 4 chars
        "description": "This is a test note",
        "category": "Home"           # ✅ REQUIRED FIELD
    }

    res = api.create_note(token, payload)

    print("CREATE RESPONSE:", res.json())  # debug

    assert res.status_code == 200

    data = res.json()
    assert "data" in data
    assert data["data"]["title"] == payload["title"]


def test_delete_note():
    api = APIClient()
    token = api.login(EMAIL, PASS)

    res = api.get_notes(token)
    assert res.status_code == 200

    notes = res.json().get("data", [])

    if not notes:
        payload = {
            "title": "Auto Note Title",   # ✅ valid
            "description": "Created for delete test",
            "category": "Work"            # ✅ REQUIRED
        }

        create_res = api.create_note(token, payload)
        print("CREATE RESPONSE:", create_res.json())

        assert create_res.status_code == 200
        note_id = create_res.json()["data"]["id"]
    else:
        note_id = notes[0]["id"]

    delete_res = api.delete_note(note_id, token)
    assert delete_res.status_code == 200


def test_invalid_token():
    api = APIClient()

    res = api.get_notes("INVALID_TOKEN")

    assert res.status_code == 401


def test_delete_invalid_id():
    api = APIClient()
    token = api.login(EMAIL, PASS)

    res = api.delete_note("999999", token)

    assert res.status_code in [400, 404]