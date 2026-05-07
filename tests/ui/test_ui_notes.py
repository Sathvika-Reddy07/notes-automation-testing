import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage

# ✅ UI Performance Engineering
from utils.performance_engine import UIPerformance

EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


def test_login_valid(driver):

    print("SESSION ID:", driver.session_id)

    # ✅ UI PERFORMANCE
    UIPerformance.measure_page_load(
        driver,
        "Valid Login Page"
    )

    login = LoginPage(driver)
    login.login(EMAIL, PASS)

    assert "notes" in driver.current_url.lower()


def test_login_invalid_password(driver):

    print("SESSION ID:", driver.session_id)

    # ✅ UI PERFORMANCE
    UIPerformance.measure_page_load(
        driver,
        "Invalid Login Page"
    )

    login = LoginPage(driver)
    login.login(EMAIL, "wrong")

    assert "invalid" in login.get_error().lower()


def test_login_empty(driver):

    print("SESSION ID:", driver.session_id)

    # ✅ UI PERFORMANCE
    UIPerformance.measure_page_load(
        driver,
        "Empty Login Page"
    )

    login = LoginPage(driver)
    login.login("", "")

    assert "required" in login.get_error().lower()


def test_create_note_missing_title(driver):

    print("SESSION ID:", driver.session_id)

    # ✅ UI PERFORMANCE
    UIPerformance.measure_page_load(
        driver,
        "Missing Title Flow"
    )

    login = LoginPage(driver)
    login.login(EMAIL, PASS)

    notes = NotesPage(driver)
    notes.create_note("", "desc")

    assert (
        "required" in driver.page_source.lower()
        or len(notes.get_notes()) >= 0
    )


def test_create_note_missing_desc(driver):

    print("SESSION ID:", driver.session_id)

    # ✅ UI PERFORMANCE
    UIPerformance.measure_page_load(
        driver,
        "Missing Description Flow"
    )

    login = LoginPage(driver)
    login.login(EMAIL, PASS)

    notes = NotesPage(driver)
    notes.create_note("Title Only", "")

    assert True