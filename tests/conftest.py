import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config
from pages.login_page import LoginPage
import os

# Setup logging configuration from custom logger utility
from utils.logger import setup_logging
setup_logging()

# Get logger instance for this module
import logging
logger = logging.getLogger(__name__)

# Create base reports directory if it doesn't exist
reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(reports_dir, exist_ok=True)

# Create screenshots directory inside reports folder
screenshots_dir = os.path.join(reports_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)


@pytest.fixture(scope="session")
def driver():
    """
    Fixture to initialize WebDriver instance based on browser from Config.
    Supports Chrome, Firefox, and Edge.
    Runs once per test session.
    """
    logger.info("Initializing browser setup...")
    logger.info(f"Selected Browser: {Config.BROWSER}")
    logger.info(f"Incognito mode enabled: {Config.INCOGNITO}")
    logger.info(f"Headless mode enabled: {Config.HEADLESS}")

    # Launch Chrome
    if Config.BROWSER.lower() == "chrome":
        logger.debug("Configuring Chrome browser options")
        options = Config.get_chrome_options()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Launch Firefox
    elif Config.BROWSER.lower() == "firefox":
        logger.debug("Configuring Firefox browser options")
        options = webdriver.FirefoxOptions()
        if Config.INCOGNITO:
            options.add_argument("-private")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    # Launch Edge
    elif Config.BROWSER.lower() == "edge":
        logger.debug("Launching Microsoft Edge browser")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    else:
        logger.error(f"Unsupported browser selected: {Config.BROWSER}")
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")

    # Apply default WebDriver configurations
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    logger.info("Browser initialized successfully and window maximized")

    yield driver  # Provide driver to test

    # Teardown
    logger.info("Closing browser instance")
    driver.quit()


@pytest.fixture
def standard_user(driver):
    """
    Fixture to log in as standard_user before a test and return ProductsPage.
    Ensures login state is reset after the test.
    """
    logger.info("Attempting login as standard_user")
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    
    from pages.products_page import ProductsPage
    products_page = ProductsPage(driver)
    
    # Wait for products page to load
    logger.debug("Waiting for Products page to load...")
    products_page.wait_for_element_to_be_present(products_page.PRODUCTS_TITLE)
    logger.info("Login successful - Products page loaded")

    yield products_page  # Provide logged-in ProductsPage object to test

    # Teardown after test execution
    try:
        if "inventory" in driver.current_url:
            logger.debug("Resetting application state from Products page")
            products_page.reset_app_state()
        else:
            logger.debug("Navigating to Products page for reset")
            driver.get("https://www.saucedemo.com/inventory.html")
            products_page.reset_app_state()
        logger.info("Application state reset successfully")
    except Exception as e:
        logger.warning(f"Could not reset app state: {e}. Navigating back to login page.")
        driver.get("https://www.saucedemo.com/")


# ---------------------- Pytest Hooks ----------------------

def pytest_configure(config):
    """Attach environment details to HTML test report."""
    logger.info("Configuring pytest environment metadata")
    config._metadata = {
        "Browser": Config.BROWSER,
        "Incognito Mode": Config.INCOGNITO,
        "Headless Mode": Config.HEADLESS,
        "Base URL": Config.BASE_URL
    }


def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "SauceDemo Automation Test Report"
    logger.info("Custom HTML report title set")


def pytest_runtest_logstart(nodeid, location):
    """Log when a test starts execution."""
    logger.info(f"Starting test execution: {nodeid}")


def pytest_runtest_logfinish(nodeid, location):
    """Log when a test finishes execution."""
    logger.info(f"Finished test execution: {nodeid}")


def pytest_runtest_logreport(report):
    """Log result of each test (pass/fail/skip)."""
    if report.failed:
        logger.error(f"Test FAILED: {report.nodeid} - {report.longreprtext}")
    elif report.passed:
        logger.info(f"Test PASSED: {report.nodeid}")
    elif report.skipped:
        logger.warning(f"Test SKIPPED: {report.nodeid}")
