import pytest
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestProductsCartIconVisibility:
    def test_cart_icon_visibility(self, standard_user):
        """
        Test-Case-4: Check cart icon visibility
        - Ensures that once a user logs in successfully, the cart icon is displayed.
        """
        logger.info("===== Starting Test: Cart Icon Visibility =====")
        products_page = standard_user
        logger.info("User logged in with standard_user credentials")

        # Verify cart icon is displayed after login
        assert products_page.is_cart_icon_visible(), "Cart icon should be visible after login"
        logger.info("Cart icon is visible as expected")

        logger.info("===== Test Completed: Cart Icon Visibility =====")
