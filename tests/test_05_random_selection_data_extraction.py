import pytest
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestProductsRandomProductSelection:
    def test_random_product_selection(self, standard_user):
        """
        Test-Case-5: Random selection of products and data extraction
        - Randomly selects 4 products
        - Extracts and logs product names and prices
        - Stores product list for use in later test cases
        """
        logger.info("===== Starting Test: Random Product Selection =====")
        products_page = standard_user

        # Randomly select 4 products
        selected_products = products_page.select_random_products(4)
        logger.debug(f"Selected products data: {selected_products}")

        # Validate that exactly 4 products were selected
        assert len(selected_products) == 4, "Should select exactly 4 products"
        logger.info(f"{len(selected_products)} products selected successfully")

        # Log product details for debugging and reporting
        for product in selected_products:
            logger.info(f"Selected product: {product['name']}, Price: ${product['price']}")

        # Store selected products in the page object for later use (e.g., cart, checkout tests)
        standard_user.selected_products = selected_products
        logger.info("Random product selection completed successfully")

        logger.info("===== Test Completed: Random Product Selection =====")
