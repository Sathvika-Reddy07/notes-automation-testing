# Importing reusable API client
# contains all API request methods
from api_client.api_client import APIClient

# Importing time module
# used for response time calculation
import time

# Importing MCP-based intelligent utilities
from utils.mcp_performance_engine import (
    LLMDataGenerator,
    PerformanceMonitor,
    FailureAnalyzer,
)

# Importing enterprise performance validation utility
from utils.performance_engine import APIPerformance


# Test account credentials
EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


# GET NOTES API TEST
# Validate notes retrieval API functionality
def test_get_notes():

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Capture API start time
    start = time.time()

    # Call GET /notes API
    res = api.get_notes(token)

    # Capture API end time
    end = time.time()

    # Calculate total response time
    response_time = end - start

    # Print response time for debugging
    print(f"Response Time: {response_time:.2f} sec")

    # MCP-based response evaluation
    # validates intelligent performance metrics
    PerformanceMonitor.evaluate_response(res)

    # Enterprise-level API performance validation
    APIPerformance.validate(
        res,
        "Get Notes API"
    )

    # Validate successful status code
    assert res.status_code == 200

    # Soft performance validation
    # ensures API is not extremely slow
    assert response_time < 20, (
        f"API too slow: {response_time:.2f} sec"
    )

    # Convert API response into JSON
    data = res.json()

    # Validate response contains "data" key
    assert "data" in data


# CREATE NOTE API TEST
# Validate note creation API
def test_create_note():

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Generate dynamic note payload using MCP LLM generator
    payload = LLMDataGenerator.generate_note()

    # Capture API start time
    start = time.time()

    try:

        # Call create note API
        res = api.create_note(token, payload)

    except Exception as e:

        # MCP intelligent failure analysis
        print(FailureAnalyzer.analyze(str(e)))

        raise

    # Capture API end time
    end = time.time()

    # Calculate total response time
    response_time = end - start

    # Print response timing
    print(f"Create Note Response Time: {response_time:.2f} sec")

    # Print API response for debugging
    print("CREATE RESPONSE:", res.json())

    # MCP-based response evaluation
    PerformanceMonitor.evaluate_response(res)

    # Enterprise-level performance validation
    APIPerformance.validate(
        res,
        "Create Note API"
    )

    # Validate successful status code
    assert res.status_code == 200

    # Validate acceptable API response time
    assert response_time < 20, (
        f"Create API too slow: {response_time:.2f} sec"
    )

    # Convert response into JSON
    data = res.json()

    # Validate response contains "data" object
    assert "data" in data

    # Validate created note title matches request payload
    assert data["data"]["title"] == payload["title"]


# DELETE NOTE API TEST
# Validate note deletion functionality
def test_delete_note():

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Fetch existing notes
    res = api.get_notes(token)

    # MCP intelligent performance monitoring
    PerformanceMonitor.evaluate_response(res)

    # Enterprise-level performance validation
    APIPerformance.validate(
        res,
        "Fetch Notes Before Delete"
    )

    # Validate successful response
    assert res.status_code == 200

    # Extract notes list from response
    notes = res.json().get("data", [])

    # If no notes exist
    if not notes:

        # Create temporary note payload
        payload = {
            "title": "Auto Note Title",
            "description": "Created for delete test",
            "category": "Work",
        }

        # Create note for delete validation
        create_res = api.create_note(token, payload)

        # Print create response for debugging
        print("CREATE RESPONSE:", create_res.json())

        # Enterprise performance validation
        APIPerformance.validate(
            create_res,
            "Create Note For Delete"
        )

        # Validate note creation success
        assert create_res.status_code == 200

        # Extract created note ID
        note_id = create_res.json()["data"]["id"]

    else:

        # Use existing note ID
        note_id = notes[0]["id"]

    # Capture delete API start time
    start = time.time()

    # Call delete note API
    delete_res = api.delete_note(note_id, token)

    # Capture delete API end time
    end = time.time()

    # Calculate delete response time
    response_time = end - start

    # Print delete API response time
    print(f"Delete Note Response Time: {response_time:.2f} sec")

    # MCP performance monitoring
    PerformanceMonitor.evaluate_response(delete_res)

    # Enterprise performance validation
    APIPerformance.validate(
        delete_res,
        "Delete Note API"
    )

    # Validate successful delete operation
    assert delete_res.status_code == 200

    # Validate acceptable delete response time
    assert response_time < 20, (
        f"Delete API too slow: {response_time:.2f} sec"
    )


# INVALID TOKEN TEST
# Validate unauthorized access handling
def test_invalid_token():

    # Create API client instance
    api = APIClient()

    # Call API using invalid authentication token
    res = api.get_notes("INVALID_TOKEN")

    # Validate unauthorized status code
    assert res.status_code == 401


# INVALID DELETE ID TEST
# Validate delete API error handling
def test_delete_invalid_id():

    # Create API client instance
    api = APIClient()

    # Generate authentication token
    token = api.login(EMAIL, PASS)

    # Attempt deleting invalid note ID
    res = api.delete_note("999999", token)

    # Validate expected failure status code
    assert res.status_code in [400, 404]