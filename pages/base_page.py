from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException
)


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # -------------------------
    # WAIT VISIBILITY
    # -------------------------
    def wait_visible(self, locator):
        for _ in range(2):
            try:
                return self.wait.until(
                    EC.visibility_of_element_located(locator)
                )
            except StaleElementReferenceException:
                continue

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # -------------------------
    # WAIT CLICKABLE
    # -------------------------
    def wait_click(self, locator):
        for _ in range(2):
            try:
                return self.wait.until(
                    EC.element_to_be_clickable(locator)
                )
            except StaleElementReferenceException:
                continue

        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # -------------------------
    # CLICK (FIXED + SAFE)
    # -------------------------
    def click(self, locator):
        for _ in range(3):
            try:
                element = self.wait_click(locator)

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                try:
                    element.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )
                return

            except StaleElementReferenceException:
                continue

        # fallback
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", element)

    # -------------------------
    # TYPE
    # -------------------------
    def type(self, locator, value):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(value)

    # -------------------------
    # TEXT
    # -------------------------
    def get_text(self, locator):
        return self.wait_visible(locator).text