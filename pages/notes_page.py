from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage


class NotesPage(BasePage):

    # -------------------------
    # LOCATORS (STABLE)
    # -------------------------
    ADD_BTN = (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Create') or contains(text(),'New')]")

    TITLE = (By.CSS_SELECTOR, "input[name='title'], input[placeholder*='Title']")

    DESCRIPTION = (By.CSS_SELECTOR, "textarea, div[contenteditable='true']")

    SAVE_BTN = (By.CSS_SELECTOR, "[data-testid='note-submit']")

    NOTE_ITEMS = (By.CSS_SELECTOR, "[data-testid='note-item-title']")

    # -------------------------
    # CREATE NOTE
    # -------------------------
    def create_note(self, title, description):

        self.click(self.ADD_BTN)

        self.wait.until(
            EC.presence_of_element_located(self.TITLE)
        )

        # TITLE
        for _ in range(2):
            try:
                title_el = self.wait_visible(self.TITLE)
                title_el.clear()
                title_el.send_keys(title)
                break
            except StaleElementReferenceException:
                continue

        # DESCRIPTION
        for _ in range(2):
            try:
                desc_el = self.wait_visible(self.DESCRIPTION)
                desc_el.clear()
                desc_el.send_keys(description)
                break
            except StaleElementReferenceException:
                continue

        # SAVE (important fix for ad overlay issue)
        save_btn = self.wait_click(self.SAVE_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)

        try:
            save_btn.click()
        except:
            # fallback for iframe/ad interference
            self.driver.execute_script("arguments[0].click();", save_btn)

    # -------------------------
    # GET NOTES (FIXED)
    # -------------------------
    def get_notes(self):
        elements = self.driver.find_elements(*self.NOTE_ITEMS)
        return [e.text.strip() for e in elements if e.text.strip()]

    # -------------------------
    # NOTE EXISTS (FIXED)
    # -------------------------
    def note_exists(self, title):
        return title.strip() in self.get_notes()