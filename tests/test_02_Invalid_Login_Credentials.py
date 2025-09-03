import pytest
from pages.login_page import LoginPage
from utils.data_reader import get_users
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestLoginInvalidCredentials:
    def test_login_with_invalid_credentials(self, driver):
        """
        Test-Case-2: Login with invalid credentials
        - Verifies that login fails with incorrect username/password
        """
        logger.info("===== Starting Test: Login with Invalid Credentials =====")

        # Initialize login page and attempt login with invalid data
        login_page = LoginPage(driver)
        login_page.login("invalid_user", "invalid_password")
        logger.info("Submitted invalid login credentials")

        # Verify error message
        error_message = login_page.get_error_message()
        logger.debug(f"Error message displayed: {error_message}")
        assert "Epic sadface: Username and password do not match any user in this service" in error_message, \
            "Invalid credentials error message not displayed"
        logger.info("Invalid credentials correctly rejected")

        logger.info("===== Test Completed: Login with Invalid Credentials =====")