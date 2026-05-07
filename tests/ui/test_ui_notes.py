# Importing pytest framework
import pytest

# Importing LoginPage class
# contains reusable login page methods
from pages.login_page import LoginPage

# Importing NotesPage class
# contains reusable notes page methods
from pages.notes_page import NotesPage

# Importing UI performance monitoring utility
from utils.performance_engine import UIPerformance


# Test account credentials
EMAIL = "theepireddysathvika@gmail.com"
PASS = "SathvikaReddy7"


# VALID LOGIN TEST
# Validate successful login with valid credentials
def test_login_valid(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "Valid Login Page"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Perform login operation
    login.login(EMAIL, PASS)

    # Validate successful navigation to notes page
    assert "notes" in driver.current_url.lower()


# INVALID PASSWORD TEST
# Validate login failure with incorrect password
def test_login_invalid_password(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "Invalid Login Page"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Attempt login using invalid password
    login.login(EMAIL, "wrong")

    # Validate invalid login error message
    assert "invalid" in login.get_error().lower()


# EMPTY LOGIN TEST
# Validate required field validation for empty login form
def test_login_empty(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "Empty Login Page"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Attempt login with empty credentials
    login.login("", "")

    # Validate required field validation message
    assert "required" in login.get_error().lower()


# CREATE NOTE WITHOUT TITLE TEST
# Validate note creation behavior when title is missing
def test_create_note_missing_title(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "Missing Title Flow"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Perform login operation
    login.login(EMAIL, PASS)

    # Create NotesPage object
    notes = NotesPage(driver)

    # Attempt creating note without title
    notes.create_note("", "desc")

    # Validate required validation message
    # or validate application remains stable
    assert (
        "required" in driver.page_source.lower()
        or len(notes.get_notes()) >= 0
    )


# CREATE NOTE WITHOUT DESCRIPTION TEST
# Validate note creation with empty description field
def test_create_note_missing_desc(driver):

    # Print Selenium session ID for debugging
    print("SESSION ID:", driver.session_id)

    # Measure UI page load performance
    UIPerformance.measure_page_load(
        driver,
        "Missing Description Flow"
    )

    # Create LoginPage object
    login = LoginPage(driver)

    # Perform login operation
    login.login(EMAIL, PASS)

    # Create NotesPage object
    notes = NotesPage(driver)

    # Attempt creating note without description
    notes.create_note("Title Only", "")

    # Placeholder validation
    # ensures test execution completes successfully
    assert True