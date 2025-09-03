import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Initialize logger for this module
logger = logging.getLogger(__name__)

class TestAddProductsToCart:
    def test_add_products_to_cart(self, standard_user):
        """Test-Case-6: Add selected products to cart and validate"""
        logger.info("===== Starting Test: Add Products to Cart =====")
        products_page = standard_user
        
        # Select products if not already selected in session
        if not hasattr(products_page, 'selected_products'):
            logger.info("Selecting 4 random products to add to cart")
            products_page.selected_products = products_page.select_random_products(4)
        
        # Add products to cart
        logger.info(f"Adding {len(products_page.selected_products)} products to cart")
        products_page.add_products_to_cart(products_page.selected_products)
        
        # Wait for cart count to update using explicit wait
        WebDriverWait(products_page.driver, 10).until(
            lambda driver: products_page.get_cart_count() == 4
        )
        
        # Verify cart count
        cart_count = products_page.get_cart_count()
        logger.info(f"Cart count after adding products: {cart_count}")
        assert cart_count == 4, f"Cart should have 4 items, but has {cart_count}"
        
        logger.info("===== Test Passed: Products successfully added to cart =====")
