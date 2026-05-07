# utils/agentic_engine.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

from selenium.webdriver.common.by import By

import time


# =========================
# SMART WAIT
# =========================
class SmartWait:

    def __init__(self, driver, timeout=25):

        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # generic until support
    def until(self, condition):
        return self.wait.until(condition)

    # visible element
    def visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # clickable element
    def clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # present element
    def present(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )


# =========================
# SELF HEALING
# =========================
class SelfHealing:

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator):

        by, value = locator

        strategies = []

        # original locator
        strategies.append(locator)

        # auto-healing strategies
        if by == By.ID:
            strategies.append(
                (By.XPATH, f"//*[@id='{value}']")
            )

        if by == By.NAME:
            strategies.append(
                (By.CSS_SELECTOR, f"[name='{value}']")
            )

        if by == By.CLASS_NAME:
            strategies.append(
                (By.CSS_SELECTOR, f".{value}")
            )

        # fallback raw css
        strategies.append((By.CSS_SELECTOR, value))

        for strat in strategies:

            try:
                return self.driver.find_element(*strat)

            except Exception:
                continue

        raise NoSuchElementException(
            f"All locator strategies failed: {locator}"
        )


# =========================
# RETRY ENGINE
# =========================
class RetryEngine:

    def __init__(self, retries=3, delay=1):

        self.retries = retries
        self.delay = delay

    def execute(self, func, *args, **kwargs):

        last_exception = None

        for _ in range(self.retries):

            try:
                return func(*args, **kwargs)

            except (
                StaleElementReferenceException,
                TimeoutException,
                WebDriverException,
            ) as e:

                last_exception = e
                time.sleep(self.delay)

        raise last_exception


# =========================
# AGENTIC ENGINE
# =========================
class AgenticEngine:

    def __init__(self, driver):

        self.driver = driver
        self.wait = SmartWait(driver)
        self.heal = SelfHealing(driver)
        self.retry = RetryEngine()

    # smart click
    def smart_click(self, locator):

        def action():

            element = self.wait.clickable(locator)
            element.click()

        self.retry.execute(action)

    # smart typing
    def smart_type(self, locator, text):

        def action():

            element = self.wait.visible(locator)

            element.clear()
            element.send_keys(text)

        self.retry.execute(action)

    # smart find
    def smart_find(self, locator):
        return self.heal.find(locator)

    # smart get text
    def smart_text(self, locator):

        def action():
            return self.wait.visible(locator).text

        return self.retry.execute(action)

    # smart visibility
    def is_visible(self, locator):

        try:
            self.wait.visible(locator)
            return True

        except Exception:
            return False