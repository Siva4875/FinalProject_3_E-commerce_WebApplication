import pytest
from pages.login_page import LoginPage
from utils.data_reader import get_users
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestLogin:
    @pytest.mark.parametrize("user", get_users())
    def test_login_with_various_users(self, driver, user):
        """
        Test-Case-1: Login with various predefined users
        - Covers standard_user, problem_user, performance_glitch_user, and locked_out_user
        - Validates successful login for valid users
        - Ensures locked out user gets proper error message
        """
        logger.info("===== Starting Test: Login with Various Users =====")
        logger.info(f"Attempting login with username: {user['username']}")

        # Initialize login page and attempt login
        login_page = LoginPage(driver)
        login_page.login(user["username"], user["password"])
        logger.info("Login form submitted")

        if user["username"] == "locked_out_user":
            # Verify error message for locked-out user
            error_message = login_page.get_error_message()
            logger.debug(f"Error message displayed: {error_message}")
            assert "Epic sadface: Sorry, this user has been locked out." in error_message, \
                "Locked out user should not be able to log in"
            logger.info("Locked out user correctly prevented from logging in")
        else:
            # Verify successful login for valid users
            from pages.products_page import ProductsPage
            products_page = ProductsPage(driver)
            page_title = products_page.get_title()
            logger.debug(f"Products Page Title: {page_title}")
            assert "Products" in page_title, f"Unexpected page title: {page_title}"
            logger.info(f"User {user['username']} successfully logged in")

            # Logout after verification to reset state
            products_page.logout()
            assert driver.current_url == "https://www.saucedemo.com/", "Logout did not return to login page"
            logger.info(f"User {user['username']} successfully logged out")

        logger.info("===== Test Completed: Login with Various Users =====")
