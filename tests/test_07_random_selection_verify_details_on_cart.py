import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Initialize logger for this module
logger = logging.getLogger(__name__)

class TestValidateCartDetails:
    def test_validate_cart_details(self, standard_user):
        """Test-Case-7: Validate product details inside the cart"""
        logger.info("===== Starting Test: Validate Cart Details =====")
        products_page = standard_user
        
        # Ensure cart has products before validation
        if not hasattr(products_page, 'selected_products') or len(products_page.selected_products) == 0:
            logger.warning("No products found in session, selecting 2 products to add")
            products_page.selected_products = products_page.select_random_products(2)
            products_page.add_products_to_cart(products_page.selected_products)
            WebDriverWait(products_page.driver, 10).until(
                lambda driver: products_page.get_cart_count() > 0
            )
        
        # Navigate to cart page
        logger.info("Navigating to cart page")
        products_page.go_to_cart()
        
        from pages.cart_page import CartPage
        cart_page = CartPage(products_page.driver)
        
        # Verify cart page title
        title = cart_page.get_title()
        logger.info(f"Cart page title: {title}")
        assert "Your Cart" in title, "Cart page title mismatch"
        
        # Wait for cart items to be visible
        cart_page.wait_for_cart_items()
        
        # Get cart items
        cart_items = cart_page.get_cart_items(timeout=15)
        logger.info(f"Number of items in cart: {len(cart_items)}")
        assert len(cart_items) > 0, "Cart should have items"
        
        # Get item names and prices
        item_names = cart_page.get_item_names(timeout=15)
        item_prices = cart_page.get_item_prices(timeout=15)
        logger.info(f"Cart item names: {item_names}")
        logger.info(f"Cart item prices: {item_prices}")
        
        # Validate expected count of items
        expected_count = len(products_page.selected_products)
        assert len(item_names) == expected_count, f"Expected {expected_count} items, found {len(item_names)}"
        assert len(item_prices) == expected_count, f"Expected {expected_count} prices, found {len(item_prices)}"
        
        # Verify product details match what was added
        for product in products_page.selected_products:
            logger.info(f"Validating product in cart: {product}")
            assert product['name'] in item_names, f"Product {product['name']} not found in cart"
            assert product['price'] in item_prices, f"Product price {product['price']} not found in cart"
        
        logger.info("===== Test Passed: Cart details validated successfully =====")
    