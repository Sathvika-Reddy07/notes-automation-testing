# Importing system-level modules
# used for dynamic path handling
import sys
import os

# Importing Path utility
# used for folder creation and path operations
from pathlib import Path


# Adding project root directory into Python path
# allows importing project modules correctly
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# Importing pytest framework
import pytest

# Importing Selenium WebDriver
from selenium import webdriver

# Importing custom logger utility
from utils.logger import get_logger

# Importing agentic automation engine
from utils.agentic_engine import AgenticEngine

# Importing MCP failure analysis utility
from utils.mcp_performance_engine import FailureAnalyzer


# SESSION START
# Executes once before test session starts
def pytest_sessionstart(session):

    try:

        # Create screenshots folder dynamically
        # stores failure screenshots and logs
        Path("logs/screenshots").mkdir(
            parents=True,
            exist_ok=True
        )

    except Exception as e:

        # Print warning if folder creation fails
        print(f"⚠️ Log folder issue: {e}")


# TEST RESULT LOGGING
# Captures test execution results
def pytest_runtest_logreport(report):

    # Create logger instance
    logger = get_logger()

    # Execute only after actual test call phase
    if report.when == "call":

        # Log passed test cases
        if report.passed:

            logger.info(
                f"PASS: {report.nodeid}"
            )

        # Log failed test cases
        elif report.failed:

            logger.error(
                f"FAIL: {report.nodeid}"
            )

            # MCP intelligent failure analysis
            analysis = FailureAnalyzer.analyze(
                str(report.longrepr)
            )

            # Log MCP analysis result
            logger.error(
                f"MCP ANALYSIS: {analysis}"
            )


# DRIVER FIXTURE
# Handles browser setup and teardown
@pytest.fixture(scope="function")
def driver():

    # Create Chrome browser options object
    options = webdriver.ChromeOptions()

    # Browser preference settings
    # used for improving automation stability
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
        "profile.managed_default_content_settings.images": 2,
    }

    # Apply browser preferences
    options.add_experimental_option(
        "prefs",
        prefs
    )

    # Disable unnecessary browser features
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Launch browser in maximized mode
    options.add_argument("--start-maximized")

    # Initialize remote WebDriver session
    # connects with Selenium Grid
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options,
    )

    # Create logger instance
    logger = get_logger()

    # Log Selenium session ID
    logger.info(
        f"SESSION STARTED: {driver.session_id}"
    )

    # Apply implicit wait
    driver.implicitly_wait(5)

    # Set maximum page load timeout
    driver.set_page_load_timeout(60)

    # Yield driver instance to test cases
    yield driver

    # Log session completion
    logger.info("SESSION ENDED")

    # Close browser session
    driver.quit()


# AGENT FIXTURE
# Provides reusable AgenticEngine object
@pytest.fixture(scope="function")
def agent(driver):

    # Return initialized agentic engine instance
    return AgenticEngine(driver)