from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

class CheckoutPage(BasePage):
    # Locators for checkout page elements
    CHECKOUT_TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        """
        Initialize CheckoutPage with WebDriver and logger.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def get_title(self):
        """
        Get the title text of the checkout page.
        """
        title = self.get_text(self.CHECKOUT_TITLE)
        self.logger.info(f"Checkout page title: {title}")
        return title
    
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """
        Fill out the checkout form with customer information.
        """
        self.send_keys(self.FIRST_NAME_FIELD, first_name)
        self.logger.info(f"Entered first name: {first_name}")
        
        self.send_keys(self.LAST_NAME_FIELD, last_name)
        self.logger.info(f"Entered last name: {last_name}")
        
        self.send_keys(self.POSTAL_CODE_FIELD, postal_code)
        self.logger.info(f"Entered postal code: {postal_code}")
    
    def continue_to_overview(self):
        """
        Click the Continue button to go to the overview page.
        """
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked Continue button on checkout page")
    
    def cancel_checkout(self):
        """
        Click the Cancel button to return to the cart page.
        """
        self.click(self.CANCEL_BUTTON)
        self.logger.info("Clicked Cancel button on checkout page")
    
    def get_error_message(self):
        """
        Get the error message text if present, otherwise return None.
        """
        if self.is_element_present(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            self.logger.warning(f"Checkout error message displayed: {error_text}")
            return error_text
        self.logger.info("No error message displayed on checkout page")
        return None
