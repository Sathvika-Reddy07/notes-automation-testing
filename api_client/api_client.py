import requests
from config.config import API_BASE_URL


class APIClient:

    def login(self, email, password):
        res = requests.post(
            f"{API_BASE_URL}/users/login",
            json={
                "email": email,
                "password": password
            }
        )

        data = res.json()
        print("LOGIN RESPONSE:", data)

        if res.status_code == 200:
            if "data" in data and "token" in data["data"]:
                return data["data"]["token"]
            elif "token" in data:
                return data["token"]

        raise Exception(f"Login failed: {data}")

    def get_notes(self, token):
        return requests.get(
            f"{API_BASE_URL}/notes",
            headers={"x-auth-token": token}
        )

    def create_note(self, token, payload):
        return requests.post(
            f"{API_BASE_URL}/notes",
            json=payload,
            headers={"x-auth-token": token}
        )

    def delete_note(self, note_id, token):
        return requests.delete(
            f"{API_BASE_URL}/notes/{note_id}",
            headers={"x-auth-token": token}
        )