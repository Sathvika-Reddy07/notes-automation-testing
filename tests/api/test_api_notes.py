from api_client.api_client import APIClient
import time

from utils.mcp_performance_engine import (
    LLMDataGenerator,
    PerformanceMonitor,
    FailureAnalyzer,
)

# ✅ Performance Engineering
from utils.performance_engine import APIPerformance


# 🔐 Credentials
EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


def test_get_notes():

    api = APIClient()
    token = api.login(EMAIL, PASS)

    start = time.time()

    res = api.get_notes(token)

    end = time.time()
    response_time = end - start

    print(f"Response Time: {response_time:.2f} sec")

    # ✅ MCP Performance Monitoring
    PerformanceMonitor.evaluate_response(res)

    # ✅ Industry Performance Engineering
    APIPerformance.validate(
        res,
        "Get Notes API"
    )

    assert res.status_code == 200

    # Soft performance validation
    assert response_time < 20, (
        f"API too slow: {response_time:.2f} sec"
    )

    data = res.json()

    assert "data" in data


def test_create_note():

    api = APIClient()
    token = api.login(EMAIL, PASS)

    # MCP LLM-style dynamic payload
    payload = LLMDataGenerator.generate_note()

    start = time.time()

    try:

        res = api.create_note(token, payload)

    except Exception as e:

        print(FailureAnalyzer.analyze(str(e)))
        raise

    end = time.time()
    response_time = end - start

    print(f"Create Note Response Time: {response_time:.2f} sec")
    print("CREATE RESPONSE:", res.json())

    # ✅ MCP Performance Monitoring
    PerformanceMonitor.evaluate_response(res)

    # ✅ Industry Performance Engineering
    APIPerformance.validate(
        res,
        "Create Note API"
    )

    assert res.status_code == 200

    assert response_time < 20, (
        f"Create API too slow: {response_time:.2f} sec"
    )

    data = res.json()

    assert "data" in data
    assert data["data"]["title"] == payload["title"]


def test_delete_note():

    api = APIClient()
    token = api.login(EMAIL, PASS)

    res = api.get_notes(token)

    # ✅ MCP Performance Monitoring
    PerformanceMonitor.evaluate_response(res)

    # ✅ Industry Performance Engineering
    APIPerformance.validate(
        res,
        "Fetch Notes Before Delete"
    )

    assert res.status_code == 200

    notes = res.json().get("data", [])

    if not notes:

        payload = {
            "title": "Auto Note Title",
            "description": "Created for delete test",
            "category": "Work",
        }

        create_res = api.create_note(token, payload)

        print("CREATE RESPONSE:", create_res.json())

        # ✅ Industry Performance Engineering
        APIPerformance.validate(
            create_res,
            "Create Note For Delete"
        )

        assert create_res.status_code == 200

        note_id = create_res.json()["data"]["id"]

    else:
        note_id = notes[0]["id"]

    start = time.time()

    delete_res = api.delete_note(note_id, token)

    end = time.time()
    response_time = end - start

    print(f"Delete Note Response Time: {response_time:.2f} sec")

    # ✅ MCP Performance Monitoring
    PerformanceMonitor.evaluate_response(delete_res)

    # ✅ Industry Performance Engineering
    APIPerformance.validate(
        delete_res,
        "Delete Note API"
    )

    assert delete_res.status_code == 200

    assert response_time < 20, (
        f"Delete API too slow: {response_time:.2f} sec"
    )


def test_invalid_token():

    api = APIClient()

    res = api.get_notes("INVALID_TOKEN")

    assert res.status_code == 401


def test_delete_invalid_id():

    api = APIClient()
    token = api.login(EMAIL, PASS)

    res = api.delete_note("999999", token)

    assert res.status_code in [400, 404]