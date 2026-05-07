from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
    element_to_be_clickable,
)
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException
)

# ⭐ Agentic imports
from utils.agentic_engine import SmartWait, RetryEngine, SelfHealing


class BasePage:

    def __init__(self, driver):
        self.driver = driver

        # 🔥 AGENTIC LAYER INTEGRATION
        self.wait = SmartWait(driver)
        self.retry = RetryEngine()
        self.heal = SelfHealing(driver)

    # -------------------------
    # WAIT VISIBLE
    # -------------------------
    def wait_visible(self, locator):
        return self.wait.visible(locator)

    # -------------------------
    # WAIT CLICKABLE
    # -------------------------
    def wait_clickable(self, locator):
        return self.wait.clickable(locator)

    # ⭐ ADDED THIS (fixes wait_click error)
    # -------------------------
    # WAIT CLICK
    # -------------------------
    def wait_click(self, locator):
        return self.wait.clickable(locator)

    # -------------------------
    # CLICK (Agentic + Safe)
    # -------------------------
    def click(self, locator):
        def action():
            element = self.wait.clickable(locator)

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

        self.retry.execute(action)

    # -------------------------
    # TYPE
    # -------------------------
    def type(self, locator, value):
        def action():
            element = self.wait.visible(locator)
            element.clear()
            element.send_keys(value)

        self.retry.execute(action)

    # -------------------------
    # GET TEXT
    # -------------------------
    def get_text(self, locator):
        return self.wait.visible(locator).text

    # -------------------------
    # SELF HEALING FIND (optional use)
    # -------------------------
    def find(self, locator):
        return self.heal.find(locator)