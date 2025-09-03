import os
from selenium.webdriver.chrome.options import Options
import logging

class Config:
    # Base URL of the application under test
    BASE_URL = "https://www.saucedemo.com/"
    
    # Browser to use for automation (chrome, firefox, edge)
    BROWSER = "chrome"
    
    # Run browser in headless mode (without UI) if set to True
    HEADLESS = False
    
    # Run browser in incognito/private mode
    INCOGNITO = True
    
    # Implicit wait (applies globally to find_element) in seconds
    IMPLICIT_WAIT = 10
    
    # Explicit wait (for specific conditions/elements) in seconds
    EXPLICIT_WAIT = 15
    
    # Path to save screenshots (inside "reports/screenshots" folder)
    SCREENSHOT_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),  # Go up two directories
        "reports",
        "screenshots"
    )
    
    # Logging level configuration (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    LOG_LEVEL = logging.INFO

    @classmethod
    def get_chrome_options(cls):
        """
        Configure Chrome browser options based on the class settings.
        Returns a configured Options object.
        """
        options = Options()
        
        # Run Chrome in headless mode (no GUI) if enabled
        if cls.HEADLESS:
            options.add_argument("--headless")
        
        # Run Chrome in incognito/private mode if enabled
        if cls.INCOGNITO:
            options.add_argument("--incognito")
        
        # Recommended flags for running Chrome in containers/CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Set browser window size
        options.add_argument("--window-size=1920,1080")
        
        return options
