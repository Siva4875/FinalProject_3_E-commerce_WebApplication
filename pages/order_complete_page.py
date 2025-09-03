from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

class OrderCompletePage(BasePage):
    # Locators for order confirmation page
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver):
        """
        Initialize OrderCompletePage with WebDriver and logger.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Order Complete Page initialized")
    
    def get_complete_header(self):
        """
        Get the header text displayed after completing an order.
        """
        header = self.get_text(self.COMPLETE_HEADER)
        self.logger.info(f"Order completion header: {header}")
        return header
    
    def get_complete_text(self):
        """
        Get the confirmation message text displayed after order completion.
        """
        text = self.get_text(self.COMPLETE_TEXT)
        self.logger.info(f"Order completion message: {text}")
        return text
    
    def back_to_home(self):
        """
        Click the 'Back Home' button to return to the products page.
        """
        self.click(self.BACK_HOME_BUTTON)
        self.logger.info("Clicked 'Back Home' button and navigating to Products page")
