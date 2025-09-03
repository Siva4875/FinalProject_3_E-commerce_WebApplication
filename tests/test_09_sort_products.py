import pytest
import logging

# Configure logger for this test module
logger = logging.getLogger(__name__)

class TestSorting:
    def test_sorting_functionality(self, standard_user):
        """
        Test-Case-9: Validate sorting functionality on the products page
        This test validates that the product sorting feature works correctly
        for the following options:
          - Name (A to Z) [default]
          - Name (Z to A)
          - Price (low to high)
          - Price (high to low)
        """
        logger.info("===== Starting Test: Sorting Functionality =====")
        products_page = standard_user
        logger.info("User logged in successfully, navigating to products page")

        # Validate default sorting: Name (A to Z)
        product_names = products_page.get_all_product_names()
        logger.debug(f"Product names (default sorting): {product_names}")
        assert product_names == sorted(product_names), "Products should be sorted by name (A to Z) by default"
        logger.info("Verified sorting by Name (A to Z)")

        # Validate sorting: Name (Z to A)
        products_page.select_sort_option("Name (Z to A)")
        product_names = products_page.get_all_product_names()
        logger.debug(f"Product names (Z to A): {product_names}")
        assert product_names == sorted(product_names, reverse=True), "Products should be sorted by name (Z to A)"
        logger.info("Verified sorting by Name (Z to A)")

        # Validate sorting: Price (low to high)
        products_page.select_sort_option("Price (low to high)")
        product_prices = products_page.get_all_product_prices()
        logger.debug(f"Product prices (low to high): {product_prices}")
        assert product_prices == sorted(product_prices), "Products should be sorted by price (low to high)"
        logger.info("Verified sorting by Price (low to high)")

        # Validate sorting: Price (high to low)
        products_page.select_sort_option("Price (high to low)")
        product_prices = products_page.get_all_product_prices()
        logger.debug(f"Product prices (high to low): {product_prices}")
        assert product_prices == sorted(product_prices, reverse=True), "Products should be sorted by price (high to low)"
        logger.info("Verified sorting by Price (high to low)")

        logger.info("All sorting options validated successfully")
        logger.info("===== Test Completed: Sorting Functionality =====")
