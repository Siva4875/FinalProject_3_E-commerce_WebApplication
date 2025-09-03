from selenium.webdriver.common.by import By
from .base_page import BasePage
from .login_page import LoginPage
import random
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage(BasePage):
    # Locators
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_LINK = (By.ID, "reset_sidebar_link")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    MENU_CONTAINER = (By.CLASS_NAME, "bm-menu-wrap")
    
    def __init__(self, driver):
        """
        Initialize ProductsPage with WebDriver and logger.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Products Page initialized")
    
    def get_title(self):
        """Get the title text on the Products page"""
        title = self.get_text(self.PRODUCTS_TITLE)
        self.logger.info(f"Products page title: {title}")
        return title
    
    def is_cart_icon_visible(self):
        """Check if the cart icon is visible"""
        visible = self.is_element_visible(self.CART_ICON)
        self.logger.info(f"Cart icon visible: {visible}")
        return visible
    
    def logout(self):
        """Logout using the sidebar menu"""
        self.logger.info("Attempting to log out...")
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        self.wait_for_url_to_be("https://www.saucedemo.com/")
        self.logger.info("Logout successful, redirected to login page")
    
    def reset_app_state(self):
        """
        Reset app state by clicking 'Reset App State' in the sidebar menu.
        Falls back to simple reset if it fails.
        """
        try:
            if "inventory" not in self.driver.current_url:
                self.logger.warning("Not on Products page. Navigating there first...")
                self.driver.get("https://www.saucedemo.com/inventory.html")
                self.wait_for_element_to_be_present(self.PRODUCTS_TITLE)
            
            self.logger.info("Opening menu for reset...")
            self.click(self.MENU_BUTTON)
            self.wait_for_element_to_be_visible(self.RESET_APP_LINK)
            
            self.click(self.RESET_APP_LINK)
            self.wait_for_element_to_be_not_visible(self.MENU_CONTAINER)
            self.wait_for_cart_to_be_empty()
            
            self.logger.info("App state reset successfully")
            return True
        except Exception as e:
            self.logger.warning(f"Reset app state failed: {e}. Trying simple reset...")
            return self.simple_reset()
    
    def simple_reset(self):
        """Reset app state by logging out and logging in again"""
        try:
            self.logger.info("Performing simple reset (logout + login)...")
            self.logout()
            
            login_page = LoginPage(self.driver)
            login_page.login("standard_user", "secret_sauce")
            self.wait_for_element_to_be_present(self.PRODUCTS_TITLE)
            
            self.logger.info("Simple reset successful")
            return True
        except Exception as e:
            self.logger.error(f"Simple reset failed: {e}")
            return False
    
    def wait_for_element_to_be_present(self, locator, timeout=10):
        """Wait until element is present in the DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"Element present: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element not present within {timeout} seconds: {locator}")
            return False
    
    def wait_for_element_to_be_visible(self, locator, timeout=10):
        """Wait until element is visible on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Element visible: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element not visible within {timeout} seconds: {locator}")
            return False
    
    def wait_for_element_to_be_not_visible(self, locator, timeout=10):
        """Wait until element is no longer visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.debug(f"Element no longer visible: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element still visible after {timeout} seconds: {locator}")
            return False
    
    def wait_for_cart_to_be_empty(self, timeout=10):
        """Wait until the cart is empty (count = 0)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.get_cart_count() == 0
            )
            self.logger.info("Cart is now empty")
            return True
        except TimeoutException:
            self.logger.warning("Cart did not reset to empty within timeout")
            return False
    
    def get_products_count(self):
        """Return the total number of products on the page"""
        count = len(self.find_elements(self.PRODUCT_ITEMS))
        self.logger.info(f"Total products found: {count}")
        return count
    
    def get_all_product_names(self):
        """Return a list of all product names"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        names = [element.text for element in elements]
        self.logger.info(f"Product names: {names}")
        return names
    
    def get_all_product_prices(self):
        """Return a list of all product prices as floats"""
        elements = self.find_elements(self.PRODUCT_PRICES)
        prices = [float(element.text.replace('$', '')) for element in elements]
        self.logger.info(f"Product prices: {prices}")
        return prices
    
    def select_random_products(self, count=4):
        """
        Randomly select 'count' number of products.
        Returns a list of dicts with product details.
        """
        products = self.find_elements(self.PRODUCT_ITEMS)
        if len(products) == 0:
            self.logger.warning("No products found on the page")
            return []
            
        selected_indices = random.sample(range(len(products)), min(count, len(products)))
        selected_products = []
        
        for idx in selected_indices:
            name = self.find_elements(self.PRODUCT_NAMES)[idx].text
            price = float(self.find_elements(self.PRODUCT_PRICES)[idx].text.replace('$', ''))
            selected_products.append({
                'name': name,
                'price': price,
                'element': products[idx],
                'index': idx
            })
        
        self.logger.info(f"Selected random products: {selected_products}")
        return selected_products
    
    def add_products_to_cart(self, products):
        """Add given list of product dicts to cart"""
        for product in products:
            add_button = product['element'].find_element(*self.ADD_TO_CART_BUTTON)
            add_button.click()
            self.logger.info(f"Added to cart: {product['name']} (${product['price']})")
    
    def get_cart_count(self):
        """Get the number of items in the cart"""
        if self.is_element_present(self.CART_ICON):
            cart_text = self.get_text(self.CART_ICON)
            count = int(cart_text) if cart_text else 0
            self.logger.info(f"Cart count: {count}")
            return count
        self.logger.warning("Cart icon not present")
        return 0
    
    def go_to_cart(self):
        """Navigate to the shopping cart page"""
        self.logger.info("Navigating to Cart page...")
        self.click(self.CART_ICON)
        self.wait_for_url_to_contain("cart")
    
    def select_sort_option(self, option):
        """Select a sorting option from the dropdown"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(self.SORT_DROPDOWN)
        select = Select(dropdown)
        
        if option.lower() == "name (a to z)":
            select.select_by_value("az")
        elif option.lower() == "name (z to a)":
            select.select_by_value("za")
        elif option.lower() == "price (low to high)":
            select.select_by_value("lohi")
        elif option.lower() == "price (high to low)":
            select.select_by_value("hilo")
        
        self.logger.info(f"Sort option selected: {option}")
