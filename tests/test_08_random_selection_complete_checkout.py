import pytest
import logging
from utils.data_reader import get_test_data
from selenium.webdriver.common.by import By

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestCheckout:
    def test_complete_checkout(self, standard_user):
        """Test-Case-8: Complete checkout and validate order"""
        logger.info("===== Starting Test: Complete Checkout =====")
        
        # Get the Products page object from the fixture (standard_user is a logged-in session)
        products_page = standard_user
        logger.info("Navigated to Products page as Standard User")

        # Select and add products to cart if not already done
        if not hasattr(products_page, 'selected_products'):
            logger.info("No products selected yet, choosing 2 random products")
            products_page.selected_products = products_page.select_random_products(2)
            products_page.add_products_to_cart(products_page.selected_products)
            logger.info(f"Added products to cart: {[p['name'] for p in products_page.selected_products]}")

        # Go to cart page
        products_page.go_to_cart()
        logger.info("Navigated to Cart page")

        from pages.cart_page import CartPage
        cart_page = CartPage(products_page.driver)

        # Proceed to checkout
        cart_page.proceed_to_checkout()
        logger.info("Proceeded to Checkout page")

        from pages.checkout_page import CheckoutPage
        checkout_page = CheckoutPage(products_page.driver)

        # Fetch checkout information from test data
        test_data = get_test_data()
        checkout_info = test_data["checkout_info"]
        logger.info(f"Using checkout data: {checkout_info}")

        # Fill in the checkout form
        checkout_page.fill_checkout_info(
            checkout_info["first_name"],
            checkout_info["last_name"],
            checkout_info["postal_code"]
        )
        logger.info("Filled in checkout details")

        # Continue to overview page
        checkout_page.continue_to_overview()
        logger.info("Navigated to Checkout: Overview page")

        # Verify overview page title
        overview_title = checkout_page.get_text((By.CLASS_NAME, "title"))
        logger.debug(f"Overview Page Title: {overview_title}")
        assert "Checkout: Overview" in overview_title, f"Unexpected overview title: {overview_title}"
        logger.info("Verified Overview page title successfully")

        # Take screenshot of order summary for reporting
        checkout_page.take_screenshot("order_summary")
        logger.info("Captured screenshot of order summary")

        # Finish checkout process
        checkout_page.click((By.ID, "finish"))
        logger.info("Clicked Finish button to place order")

        # Verify order completion page
        from pages.order_complete_page import OrderCompletePage
        order_complete_page = OrderCompletePage(products_page.driver)
        complete_header = order_complete_page.get_complete_header()
        logger.debug(f"Order Complete Header: {complete_header}")
        assert "Thank you for your order!" in complete_header, "Order confirmation message not found!"
        logger.info("Order completed successfully and verified confirmation message")

        logger.info("===== Test Completed: Complete Checkout =====")
