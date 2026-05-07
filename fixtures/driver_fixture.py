# Importing pytest framework
import pytest

# Importing Selenium WebDriver
from selenium import webdriver

# Importing Service class for Selenium 4 driver initialization
from selenium.webdriver.chrome.service import Service

# Automatically manages ChromeDriver installation
from webdriver_manager.chrome import ChromeDriverManager

# Importing application base URL from config file
from config.config import BASE_URL


# Pytest fixture used for browser setup and teardown
@pytest.fixture
def driver():

    # Creating Chrome browser options object
    options = webdriver.ChromeOptions()

    # Launch browser in maximized mode
    options.add_argument("--start-maximized")

    # Disable browser notifications and popups
    options.add_argument("--disable-notifications")

    # Selenium 4 recommended driver service syntax
    # Automatically downloads compatible ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Launch Chrome browser with service and options
    driver = webdriver.Chrome(service=service, options=options)

    # Open application URL
    driver.get(BASE_URL)

    # Ensure browser viewport zoom level is 100%
    # Helps avoid UI alignment issues during automation
    driver.execute_script("document.body.style.zoom='100%'")

    # Yield driver instance to test cases
    yield driver

    # Close browser after test execution completes
    driver.quit()