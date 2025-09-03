import pytest
from pages.login_page import LoginPage
from utils.data_reader import get_users
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestLogout:
    def test_logout_functionality(self, driver, standard_user):
        """
        Test-Case-3: Validate logout functionality
        - Logs in with a valid standard user
        - Verifies cart icon (post-login indicator)
        - Performs logout and checks URL reset
        """
        logger.info("===== Starting Test: Logout Functionality =====")

        # Standard_user fixture provides a logged-in Products page
        products_page = standard_user
        logger.info("User logged in with standard_user credentials")

        # Verify user is logged in by checking cart icon
        assert products_page.is_cart_icon_visible(), "Cart icon should be visible after login"
        logger.info("Verified cart icon is visible after login")

        # Perform logout
        products_page.logout()
        logger.info("User clicked logout")

        # Verify user is redirected to login page
        assert driver.current_url == "https://www.saucedemo.com/", "Logout did not redirect to login page"
        logger.info("Logout functionality works correctly")

        logger.info("===== Test Completed: Logout Functionality =====")
    