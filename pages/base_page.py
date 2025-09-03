from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import os
from datetime import datetime
import logging

class BasePage:
    def __init__(self, driver):
        """
        Base class for all page objects.
        Provides reusable methods for interacting with web elements.
        """
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger for debugging
    
    def find_element(self, locator, timeout=10):
        """
        Wait until the element is visible on the page and return it.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element {locator} not found within {timeout} seconds")
            raise
    
    def find_elements(self, locator, timeout=10):
        """
        Wait until multiple elements are visible and return them as a list.
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_any_elements_located(locator)
            )
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements {locator} not found within {timeout} seconds")
            raise
    
    def click(self, locator, timeout=10):
        """
        Click an element. Handles stale element exceptions by retrying once.
        """
        element = self.find_element(locator, timeout)
        try:
            element.click()
            self.logger.debug(f"Clicked element: {locator}")
        except StaleElementReferenceException:
            # Retry if element reference becomes stale
            self.logger.warning(f"Element became stale, retrying: {locator}")
            element = self.find_element(locator, timeout)
            element.click()
            self.logger.debug(f"Clicked element after retry: {locator}")
    
    def send_keys(self, locator, text, timeout=10):
        """
        Clear the input field and send text to it.
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"Entered text '{text}' in element: {locator}")
    
    def get_text(self, locator, timeout=10):
        """
        Get and return the text content of an element.
        """
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Got text '{text}' from element: {locator}")
        return text
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if an element is present in the DOM (not necessarily visible).
        """
        try:
            self.find_element(locator, timeout)
            self.logger.debug(f"Element present: {locator}")
            return True
        except (TimeoutException, NoSuchElementException):
            self.logger.debug(f"Element not present: {locator}")
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if an element is visible on the page.
        """
        try:
            element = self.find_element(locator, timeout)
            visible = element.is_displayed()
            self.logger.debug(f"Element visible {visible}: {locator}")
            return visible
        except (TimeoutException, NoSuchElementException):
            self.logger.debug(f"Element not visible: {locator}")
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Wait until an element becomes invisible or is removed from the DOM.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element {locator} did not disappear within {timeout} seconds")
            return False
    
    def wait_for_url_to_contain(self, text, timeout=10):
        """
        Wait until the current URL contains the given substring.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            self.logger.debug(f"URL contains '{text}'")
            return True
        except TimeoutException:
            self.logger.warning(f"URL did not contain '{text}' within {timeout} seconds")
            return False
    
    def wait_for_url_to_be(self, url, timeout=10):
        """
        Wait until the current URL exactly matches the expected URL.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
            self.logger.debug(f"URL is '{url}'")
            return True
        except TimeoutException:
            self.logger.warning(f"URL did not become '{url}' within {timeout} seconds")
            return False
    
    def take_screenshot(self, name):
        """
        Capture a screenshot with a timestamp and save it in the reports/screenshots folder.
        Returns the file path of the saved screenshot.
        """
        # Create a timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        
        # Define screenshot storage path
        filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "reports", 
            "screenshots", 
            filename
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save screenshot
        self.driver.save_screenshot(filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath
