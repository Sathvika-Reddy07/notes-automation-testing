# Importing Selenium locator strategy class
from selenium.webdriver.common.by import By

# Importing Selenium expected conditions
# used for explicit waits
from selenium.webdriver.support import expected_conditions as EC

# Importing stale element exception
# used for handling dynamic DOM refresh issues
from selenium.common.exceptions import StaleElementReferenceException

# Importing BasePage parent class
# contains reusable Selenium methods
from pages.base_page import BasePage


# NotesPage class handles all Notes page operations
class NotesPage(BasePage):

    # LOCATORS (STABLE)

    # Add/Create/New note button locator
    ADD_BTN = (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Create') or contains(text(),'New')]")

    # Note title input field locator
    TITLE = (By.CSS_SELECTOR, "input[name='title'], input[placeholder*='Title']")

    # Note description textarea locator
    DESCRIPTION = (By.CSS_SELECTOR, "textarea, div[contenteditable='true']")

    # Save note button locator
    SAVE_BTN = (By.CSS_SELECTOR, "[data-testid='note-submit']")

    # Notes list locator
    # Fetches all visible note titles
    NOTE_ITEMS = (By.CSS_SELECTOR, "[data-testid='note-item-title']")

    # CREATE NOTE
    # Creates a new note through UI
    def create_note(self, title, description):

        # Click Add/Create note button
        self.click(self.ADD_BTN)

        # Wait until title field is present in DOM
        self.wait.until(
            EC.presence_of_element_located(self.TITLE)
        )

        # TITLE HANDLING

        # Retry loop for stale element issues
        for _ in range(2):

            try:
                # Wait until title field becomes visible
                title_el = self.wait_visible(self.TITLE)

                # Clear existing text
                title_el.clear()

                # Enter note title
                title_el.send_keys(title)

                break

            except StaleElementReferenceException:

                # Retry if DOM refresh causes stale element
                continue

        # DESCRIPTION HANDLING

        # Retry loop for stale element issues
        for _ in range(2):

            try:
                # Wait until description field becomes visible
                desc_el = self.wait_visible(self.DESCRIPTION)

                # Clear existing text
                desc_el.clear()

                # Enter note description
                desc_el.send_keys(description)

                break

            except StaleElementReferenceException:

                # Retry if DOM refresh causes stale element
                continue

        # SAVE BUTTON HANDLING

        # Wait until save button becomes clickable
        save_btn = self.wait_click(self.SAVE_BTN)

        # Scroll button into viewport center
        # improves click stability
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)

        try:
            # Normal Selenium click
            save_btn.click()

        except:

            # JavaScript click fallback
            # handles iframe/ad overlay interference
            self.driver.execute_script("arguments[0].click();", save_btn)

    # GET NOTES
    # Fetch all visible notes from UI
    def get_notes(self):

        # Find all note title elements
        elements = self.driver.find_elements(*self.NOTE_ITEMS)

        # Return cleaned note titles list
        return [e.text.strip() for e in elements if e.text.strip()]

    # NOTE EXISTS
    # Validate whether specific note exists in UI
    def note_exists(self, title):

        # Compare title against notes list
        return title.strip() in self.get_notes()