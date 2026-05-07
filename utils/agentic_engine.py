# utils/agentic_engine.py

# Importing Selenium explicit wait utility
from selenium.webdriver.support.ui import WebDriverWait

# Importing Selenium expected conditions
# used for dynamic element waits
from selenium.webdriver.support import expected_conditions as EC

# Importing Selenium exceptions
# used for retry handling and stability improvements
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

# Importing Selenium locator strategy class
from selenium.webdriver.common.by import By

# Importing time module
# used for retry delay handling
import time


# SMART WAIT
# Handles intelligent explicit waits
class SmartWait:

    # Constructor method
    # initializes WebDriverWait instance
    def __init__(self, driver, timeout=25):

        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Generic until method
    # supports custom expected conditions
    def until(self, condition):
        return self.wait.until(condition)

    # Visible element wait
    # waits until element becomes visible
    def visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # Clickable element wait
    # waits until element becomes clickable
    def clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # Present element wait
    # waits until element exists in DOM
    def present(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )


# SELF HEALING
# Handles fallback locator recovery mechanism
class SelfHealing:

    # Constructor method
    # initializes WebDriver instance
    def __init__(self, driver):
        self.driver = driver

    # Intelligent element finder
    # automatically tries multiple locator strategies
    def find(self, locator):

        # Extract locator strategy and locator value
        by, value = locator

        # List of fallback locator strategies
        strategies = []

        # Add original locator strategy
        strategies.append(locator)

        # Auto-healing strategy for ID locator
        if by == By.ID:
            strategies.append(
                (By.XPATH, f"//*[@id='{value}']")
            )

        # Auto-healing strategy for NAME locator
        if by == By.NAME:
            strategies.append(
                (By.CSS_SELECTOR, f"[name='{value}']")
            )

        # Auto-healing strategy for CLASS locator
        if by == By.CLASS_NAME:
            strategies.append(
                (By.CSS_SELECTOR, f".{value}")
            )

        # Fallback raw CSS selector strategy
        strategies.append((By.CSS_SELECTOR, value))

        # Iterate through all locator strategies
        for strat in strategies:

            try:
                # Attempt locating element
                return self.driver.find_element(*strat)

            except Exception:

                # Continue trying next locator strategy
                continue

        # Raise exception if all locator strategies fail
        raise NoSuchElementException(
            f"All locator strategies failed: {locator}"
        )


# RETRY ENGINE
# Handles flaky UI retries automatically
class RetryEngine:

    # Constructor method
    # initializes retry count and delay
    def __init__(self, retries=3, delay=1):

        self.retries = retries
        self.delay = delay

    # Retry wrapper method
    # executes function multiple times if failure occurs
    def execute(self, func, *args, **kwargs):

        # Store latest exception
        last_exception = None

        # Retry loop
        for _ in range(self.retries):

            try:
                # Execute target function
                return func(*args, **kwargs)

            except (
                StaleElementReferenceException,
                TimeoutException,
                WebDriverException,
            ) as e:

                # Store latest failure exception
                last_exception = e

                # Wait before retrying
                time.sleep(self.delay)

        # Raise final exception after retries exhausted
        raise last_exception


# AGENTIC ENGINE
# Central intelligent automation engine
class AgenticEngine:

    # Constructor method
    # initializes reusable agentic utilities
    def __init__(self, driver):

        self.driver = driver

        # Smart wait utility
        self.wait = SmartWait(driver)

        # Self-healing locator utility
        self.heal = SelfHealing(driver)

        # Retry execution utility
        self.retry = RetryEngine()

    # SMART CLICK
    # Retry-enabled intelligent click method
    def smart_click(self, locator):

        # Inner retry action
        def action():

            # Wait until element becomes clickable
            element = self.wait.clickable(locator)

            # Perform click action
            element.click()

        # Execute action using retry engine
        self.retry.execute(action)

    # SMART TYPE
    # Retry-enabled intelligent typing method
    def smart_type(self, locator, text):

        # Inner retry action
        def action():

            # Wait until element becomes visible
            element = self.wait.visible(locator)

            # Clear existing text
            element.clear()

            # Enter new text value
            element.send_keys(text)

        # Execute typing action using retry engine
        self.retry.execute(action)

    # SMART FIND
    # Intelligent locator recovery method
    def smart_find(self, locator):
        return self.heal.find(locator)

    # SMART GET TEXT
    # Retry-enabled text extraction method
    def smart_text(self, locator):

        # Inner retry action
        def action():
            return self.wait.visible(locator).text

        # Execute text extraction using retry engine
        return self.retry.execute(action)

    # SMART VISIBILITY CHECK
    # Validates whether element is visible
    def is_visible(self, locator):

        try:
            # Wait until element becomes visible
            self.wait.visible(locator)

            return True

        except Exception:

            # Return False if element is not visible
            return False