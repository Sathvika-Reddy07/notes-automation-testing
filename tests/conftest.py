import pytest
from selenium import webdriver
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()

    # ✅ BLOCK ADS / POPUPS / NOTIFICATIONS
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
        "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)

    # ✅ STABILITY OPTIONS
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    # ✅ HANDLE ADS IFRAME ISSUE (IMPORTANT)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    # ✅ ADDED DEBUG LINE (IMPORTANT FOR ISOLATION CHECK)
    print("🧪 DRIVER SESSION ID:", driver.session_id)

    # ✅ GLOBAL TIMEOUTS
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(30)

    yield driver

    # ✅ CLEANUP AFTER TEST
    driver.quit()