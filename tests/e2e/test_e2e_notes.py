from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from api_client.api_client import APIClient

EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


def test_ui_to_api(driver):
    print("SESSION ID:", driver.session_id)   # 👈 ADD HERE

    login = LoginPage(driver)
    login.login(EMAIL, PASS)

    notes = NotesPage(driver)
    notes.create_note("Meeting Notes", "Discuss roadmap")

    api = APIClient()
    token = api.login(EMAIL, PASS)

    data = api.get_notes(token).json()["data"]
    assert any(n["title"] == "Meeting Notes" for n in data)


def test_api_to_ui(driver):
    print("SESSION ID:", driver.session_id)   # 👈 ADD HERE
    
    api = APIClient()
    token = api.login(EMAIL, PASS)

    notes = api.get_notes(token).json().get("data", [])

    # ✅ FIX: ensure note exists
    if not notes:
        payload = {
            "title": "Auto UI Note",
            "description": "Created for UI test",
            "category": "Work"
        }
        res = api.create_note(token, payload)
        assert res.status_code == 200

        note_id = res.json()["data"]["id"]
        title = res.json()["data"]["title"]
    else:
        note_id = notes[0]["id"]
        title = notes[0]["title"]

    api.delete_note(note_id, token)

    login = LoginPage(driver)
    login.login(EMAIL, PASS)

    ui_notes = NotesPage(driver)
    assert not ui_notes.note_exists(title)