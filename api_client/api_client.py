# Importing requests library to perform API calls
import requests

# Importing base API URL from centralized config file
from config.config import API_BASE_URL


# API Client class contains reusable API methods
# used throughout the automation framework
class APIClient:

    # LOGIN API
    # This method performs login operation
    # and returns authentication token
    def login(self, email, password):

        # Sending POST request to login endpoint
        res = requests.post(
            f"{API_BASE_URL}/users/login",

            # Login request payload
            json={
                "email": email,
                "password": password
            }
        )

        # Convert API response into JSON format
        data = res.json()

        # Print login response for debugging purpose
        print("LOGIN RESPONSE:", data)

        # Validate successful login status code
        if res.status_code == 200:

            # Scenario 1:
            # Token available inside "data" object
            if "data" in data and "token" in data["data"]:
                return data["data"]["token"]

            # Scenario 2:
            # Token available directly in response
            elif "token" in data:
                return data["token"]

        # Raise exception if login fails
        raise Exception(f"Login failed: {data}")

    # GET NOTES API
    # Fetch all notes for authenticated user
    def get_notes(self, token):

        # Sending GET request to notes endpoint
        return requests.get(
            f"{API_BASE_URL}/notes",

            # Passing authentication token in request header
            headers={"x-auth-token": token}
        )

    # CREATE NOTE API
    # Create a new note using API
    def create_note(self, token, payload):

        # Sending POST request with note payload
        return requests.post(
            f"{API_BASE_URL}/notes",

            # JSON request body
            json=payload,

            # Authentication token header
            headers={"x-auth-token": token}
        )

    # DELETE NOTE API
    # Delete note using note ID
    def delete_note(self, note_id, token):

        # Sending DELETE request to specific note endpoint
        return requests.delete(
            f"{API_BASE_URL}/notes/{note_id}",

            # Authentication token header
            headers={"x-auth-token": token}
        )