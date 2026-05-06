import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import BASE_URL

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    # Full screen
    options.add_argument("--start-maximized")

    # Disable popups
    options.add_argument("--disable-notifications")

    # ✅ Correct Selenium 4 syntax
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(BASE_URL)

    # Ensure full viewport
    driver.execute_script("document.body.style.zoom='100%'")

    yield driver

    driver.quit()