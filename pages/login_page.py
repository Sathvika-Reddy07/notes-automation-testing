from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class LoginPage(BasePage):

    # -------------------------
    # LOCATORS
    # -------------------------
    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")

    LOGIN_BTN = (By.CSS_SELECTOR, "[data-testid='login-submit']")

    ERROR_MSG = (
        By.XPATH,
        "//*[contains(@class,'alert') "
        "or contains(@class,'error') "
        "or contains(@role,'alert') "
        "or contains(text(),'Invalid') "
        "or contains(text(),'required')]"
    )

    # -------------------------
    # OPEN PAGE
    # -------------------------
    def open(self):
        self.driver.get("https://practice.expandtesting.com/notes/app/login")

    # -------------------------
    # LOGIN FLOW (AGENTIC SAFE)
    # -------------------------
    def login(self, email, password):
        self.open()

        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)

        self.click(self.LOGIN_BTN)

    # -------------------------
    # ERROR HANDLING
    # -------------------------
    def get_error(self):
        try:
            return self.wait.visible(self.ERROR_MSG).text
        except TimeoutException:
            return self.driver.page_source