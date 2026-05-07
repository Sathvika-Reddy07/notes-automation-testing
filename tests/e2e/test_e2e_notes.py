# Importing LoginPage class
# contains reusable login page methods
from pages.login_page import LoginPage

# Importing NotesPage class
# contains reusable notes page methods
from pages.notes_page import NotesPage

# Importing reusable API client
# used for API operations
from api_client.api_client import APIClient

# Importing UI performance monitoring utility
from utils.performance_engine import UIPerformance


# Test account credentials
EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


# UI TO API HYBRID TEST
# Validate note created in UI appears in API response
def test_ui_to_api(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "UI To API Flow"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Perform login operation
    login.login(EMAIL, PASS)

    # Create NotesPage object
    notes = NotesPage(driver)

    # Create note through UI
    notes.create_note("Meeting Notes", "Discuss roadmap")

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Fetch notes using API
    data = api.get_notes(token).json()["data"]

    # Validate UI-created note exists in API response
    assert any(
        n["title"] == "Meeting Notes"
        for n in data
    )


# API TO UI HYBRID TEST
# Validate API changes reflect correctly in UI
def test_api_to_ui(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "API To UI Flow"
    )

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Fetch all notes using API
    notes = api.get_notes(token).json().get("data", [])

    # If notes are not available
    if not notes:

        # Create temporary note payload
        payload = {
            "title": "Auto UI Note",
            "description": "Created for UI test",
            "category": "Work"
        }

        # Create note through API
        res = api.create_note(token, payload)

        # Validate successful note creation
        assert res.status_code == 200

        # Extract created note ID
        note_id = res.json()["data"]["id"]

        # Extract created note title
        title = res.json()["data"]["title"]

    else:

        # Use existing note ID
        note_id = notes[0]["id"]

        # Use existing note title
        title = notes[0]["title"]

    # Delete note through API
    api.delete_note(note_id, token)

    # Create LoginPage object
    login = LoginPage(driver)

    # Perform login operation
    login.login(EMAIL, PASS)

    # Create NotesPage object
    ui_notes = NotesPage(driver)

    # Validate deleted note no longer exists in UI
    assert not ui_notes.note_exists(title)