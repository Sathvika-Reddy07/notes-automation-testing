# Importing locator strategy class from Selenium
from selenium.webdriver.common.by import By

# Importing Selenium expected conditions
# used for explicit waits
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
    element_to_be_clickable,
)

# Importing Selenium exceptions
# used for handling flaky UI behavior
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException
)

# Agentic framework imports
# SmartWait -> intelligent waits
# RetryEngine -> retry failed UI actions
# SelfHealing -> fallback locator mechanism
from utils.agentic_engine import SmartWait, RetryEngine, SelfHealing


# BasePage acts as parent class
# for all page object classes
class BasePage:

    # Constructor method
    # initializes driver and reusable utilities
    def __init__(self, driver):
        self.driver = driver

        # AGENTIC LAYER INTEGRATION

        # Smart wait utility for dynamic waits
        self.wait = SmartWait(driver)

        # Retry utility for flaky UI operations
        self.retry = RetryEngine()

        # Self-healing locator engine
        self.heal = SelfHealing(driver)

    # WAIT VISIBLE
    # Wait until element becomes visible on UI
    def wait_visible(self, locator):
        return self.wait.visible(locator)

    # WAIT CLICKABLE
    # Wait until element becomes clickable
    def wait_clickable(self, locator):
        return self.wait.clickable(locator)

    # WAIT CLICK
    # Additional reusable clickable wait method
    # used to avoid wait_click related issues
    def wait_click(self, locator):
        return self.wait.clickable(locator)

    # CLICK METHOD
    # Agentic-safe click implementation
    # includes retries and JS fallback
    def click(self, locator):

        # Inner action method passed into retry engine
        def action():

            # Wait until element is clickable
            element = self.wait.clickable(locator)

            # Scroll element into center viewport
            # improves click stability
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            try:
                # Normal Selenium click
                element.click()

            except ElementClickInterceptedException:

                # JavaScript click fallback
                # handles overlay/intercept issues
                self.driver.execute_script("arguments[0].click();", element)

        # Retry execution if flaky failure occurs
        self.retry.execute(action)

    # TYPE METHOD
    # Used for entering text into input fields
    def type(self, locator, value):

        # Retry-enabled typing action
        def action():

            # Wait until element becomes visible
            element = self.wait.visible(locator)

            # Clear existing text before typing
            element.clear()

            # Enter new value
            element.send_keys(value)

        # Execute action using retry engine
        self.retry.execute(action)

    # GET TEXT METHOD
    # Fetch visible text from UI element
    def get_text(self, locator):
        return self.wait.visible(locator).text

    # SELF HEALING FIND METHOD
    # Uses intelligent locator recovery mechanism
    def find(self, locator):
        return self.heal.find(locator)