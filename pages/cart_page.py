from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class CartPage(BasePage):
    # Locators for Cart Page
    CART_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CLASS_NAME, "cart_button")
    
    def __init__(self, driver):
        """
        Initialize CartPage with driver and logger.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def get_title(self):
        """
        Get the page title displayed in the cart.
        """
        title = self.get_text(self.CART_TITLE)
        self.logger.info(f"Cart page title: {title}")
        return title
    
    def wait_for_cart_items(self, timeout=15):
        """
        Wait until at least one cart item is visible.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(self.get_cart_items(timeout=5)) > 0
            )
            self.logger.info("Cart items are visible on the page")
            return True
        except TimeoutException:
            self.logger.warning("No cart items found within timeout")
            return False
    
    def get_cart_items(self, timeout=10):
        """
        Return all cart item elements.
        """
        try:
            items = self.find_elements(self.CART_ITEMS, timeout)
            self.logger.info(f"Found {len(items)} cart items")
            return items
        except Exception as e:
            self.logger.warning(f"Could not find cart items: {e}")
            return []
    
    def get_item_names(self, timeout=10):
        """
        Get names of all items in the cart.
        """
        try:
            elements = self.find_elements(self.ITEM_NAMES, timeout)
            names = [element.text for element in elements]
            self.logger.info(f"Cart item names: {names}")
            return names
        except Exception as e:
            self.logger.warning(f"Could not find item names: {e}")
            return []
    
    def get_item_prices(self, timeout=10):
        """
        Get prices of all items in the cart as floats.
        """
        try:
            elements = self.find_elements(self.ITEM_PRICES, timeout)
            prices = [float(element.text.replace('$', '')) for element in elements]
            self.logger.info(f"Cart item prices: {prices}")
            return prices
        except Exception as e:
            self.logger.warning(f"Could not find item prices: {e}")
            return []
    
    def proceed_to_checkout(self):
        """
        Click the checkout button and wait until URL changes to checkout page.
        """
        self.click(self.CHECKOUT_BUTTON)
        self.logger.info("Clicked on Checkout button")
        self.wait_for_url_to_contain("checkout")
    
    def continue_shopping(self):
        """
        Click the continue shopping button and wait until redirected to inventory page.
        """
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.logger.info("Clicked on Continue Shopping button")
        self.wait_for_url_to_contain("inventory")
    
    def remove_item(self, index=0):
        """
        Remove an item from the cart based on its index (default first item).
        """
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        if index < len(remove_buttons):
            remove_buttons[index].click()
            self.logger.info(f"Removed item at index {index}")
        else:
            self.logger.warning(f"Tried to remove item at index {index}, but only {len(remove_buttons)} items exist")
    
    def is_cart_empty(self):
        """
        Check if the cart is empty.
        """
        empty = len(self.get_cart_items(timeout=5)) == 0
        self.logger.info(f"Cart empty status: {empty}")
        return empty
