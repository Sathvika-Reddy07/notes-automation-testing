# Importing Selenium locator strategy class
from selenium.webdriver.common.by import By

# Importing timeout exception
# used for handling wait failures
from selenium.common.exceptions import TimeoutException

# Importing BasePage parent class
# contains reusable Selenium utilities
from pages.base_page import BasePage


# LoginPage class handles all login page operations
class LoginPage(BasePage):

    # LOCATORS

    # Email input field locator
    EMAIL = (By.NAME, "email")

    # Password input field locator
    PASSWORD = (By.NAME, "password")

    # Login button locator
    LOGIN_BTN = (By.CSS_SELECTOR, "[data-testid='login-submit']")

    # Error message locator
    # Handles alert, validation, invalid login, and required field messages
    ERROR_MSG = (
        By.XPATH,
        "//*[contains(@class,'alert') "
        "or contains(@class,'error') "
        "or contains(@role,'alert') "
        "or contains(text(),'Invalid') "
        "or contains(text(),'required')]"
    )

    # OPEN PAGE
    # Opens Notes application login page
    def open(self):
        self.driver.get("https://practice.expandtesting.com/notes/app/login")

    # LOGIN FLOW
    # Performs complete login workflow
    # using agentic-safe reusable methods
    def login(self, email, password):

        # Open login page
        self.open()

        # Enter email into email field
        self.type(self.EMAIL, email)

        # Enter password into password field
        self.type(self.PASSWORD, password)

        # Click login button
        self.click(self.LOGIN_BTN)

    # ERROR HANDLING
    # Fetch login validation or error message
    def get_error(self):

        try:
            # Wait until error message becomes visible
            return self.wait.visible(self.ERROR_MSG).text

        except TimeoutException:

            # Fallback:
            # Return full page source for debugging
            return self.driver.page_source