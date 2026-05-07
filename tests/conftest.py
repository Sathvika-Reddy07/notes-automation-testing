import sys
import os

from pathlib import Path

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pytest

from selenium import webdriver

from utils.logger import get_logger
from utils.agentic_engine import AgenticEngine
from utils.mcp_performance_engine import FailureAnalyzer


# ==============================
# SESSION START
# ==============================
def pytest_sessionstart(session):

    try:

        Path("logs/screenshots").mkdir(
            parents=True,
            exist_ok=True
        )

    except Exception as e:

        print(f"⚠️ Log folder issue: {e}")


# ==============================
# TEST RESULT LOGGING
# ==============================
def pytest_runtest_logreport(report):

    logger = get_logger()

    if report.when == "call":

        if report.passed:

            logger.info(
                f"PASS: {report.nodeid}"
            )

        elif report.failed:

            logger.error(
                f"FAIL: {report.nodeid}"
            )

            # MCP failure analysis
            analysis = FailureAnalyzer.analyze(
                str(report.longrepr)
            )

            logger.error(
                f"MCP ANALYSIS: {analysis}"
            )


# ==============================
# DRIVER FIXTURE
# ==============================
@pytest.fixture(scope="function")
def driver():

    options = webdriver.ChromeOptions()

    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
        "profile.managed_default_content_settings.images": 2,
    }

    options.add_experimental_option(
        "prefs",
        prefs
    )

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options,
    )

    logger = get_logger()

    logger.info(
        f"SESSION STARTED: {driver.session_id}"
    )

    driver.implicitly_wait(5)

    driver.set_page_load_timeout(60)

    yield driver

    logger.info("SESSION ENDED")

    driver.quit()


# ==============================
# AGENT FIXTURE
# ==============================
@pytest.fixture(scope="function")
def agent(driver):

    return AgenticEngine(driver)