from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

class LoginPage(BasePage):
    # Locators for login page elements
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        """
        Initialize LoginPage with WebDriver and open the login page.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.driver.get("https://www.saucedemo.com/")
        self.logger.info("Navigated to SauceDemo login page")
    
    def login(self, username, password):
        """
        Perform login action using provided username and password.
        """
        self.send_keys(self.USERNAME_FIELD, username)
        self.logger.info(f"Entered username: {username}")
        
        self.send_keys(self.PASSWORD_FIELD, password)
        self.logger.info("Entered password: [HIDDEN]")
        
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked Login button")
    
    def get_error_message(self):
        """
        Return the error message text if displayed, else None.
        """
        if self.is_element_present(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            self.logger.warning(f"Login error displayed: {error_text}")
            return error_text
        self.logger.info("No error message displayed on login page")
        return None
