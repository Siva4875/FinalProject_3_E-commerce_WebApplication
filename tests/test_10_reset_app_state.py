import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Initialize logger for this module
logger = logging.getLogger(__name__)

class TestResetAppState:
    def test_reset_app_state(self, standard_user):
        """Test-Case-10: Validate 'Reset App State' functionality"""
        logger.info("===== Starting Test: Reset App State =====")
        products_page = standard_user
        
        # Add some products if none selected
        if not hasattr(products_page, 'selected_products'):
            logger.info("Selecting 2 random products before reset test")
            products_page.selected_products = products_page.select_random_products(2)
        
        logger.info(f"Adding {len(products_page.selected_products)} products to cart before reset")
        products_page.add_products_to_cart(products_page.selected_products)
        
        # Wait for cart update
        WebDriverWait(products_page.driver, 10).until(
            lambda driver: products_page.get_cart_count() > 0
        )
        
        # Verify cart has items
        cart_count = products_page.get_cart_count()
        logger.info(f"Cart count before reset: {cart_count}")
        assert cart_count > 0, "Cart should have items before reset"
        
        # Perform reset app state
        logger.info("Performing 'Reset App State'")
        success = products_page.reset_app_state()
        if success:
            logger.info("Reset App State executed successfully")
        else:
            logger.warning("Reset App State may not have executed correctly")
        
        # Wait until cart count is reset to 0
        WebDriverWait(products_page.driver, 10).until(
            lambda driver: products_page.get_cart_count() == 0
        )
        
        cart_count_after_reset = products_page.get_cart_count()
        logger.info(f"Cart count after reset: {cart_count_after_reset}")
        assert cart_count_after_reset == 0, f"Cart should be empty after reset, but has {cart_count_after_reset} items"
        
        logger.info("===== Test Passed: Reset App State functionality works correctly =====")
