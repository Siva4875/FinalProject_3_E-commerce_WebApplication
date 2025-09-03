import logging
from datetime import datetime

def setup_logging():
    """
    Configure logging for the test framework.
    
    - Logs will be written both to a file (test_execution.log) and the console.
    - Log format includes timestamp, module name, log level, and message.
    - Default log level is INFO (can be adjusted if needed).
    """
    logging.basicConfig(
        level=logging.INFO,  # Set default logging level to INFO
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define log format
        handlers=[
            logging.FileHandler("test_execution.log"),  # Save logs to file
            logging.StreamHandler()                     # Also print logs to console
        ]
    )


def take_screenshot(driver, name):
    """
    Capture and save a screenshot of the current browser state.
    
    Args:
        driver: Selenium WebDriver instance.
        name (str): Custom name for the screenshot (usually the test name).
    
    Returns:
        str: Full file path of the saved screenshot.
    """
    # Create a unique filename using the provided name and a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = f"reports/screenshots/{filename}"
    
    # Ensure the 'reports/screenshots' directory exists before saving
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save screenshot to the defined filepath
    driver.save_screenshot(filepath)
    logging.info(f"Screenshot saved: {filepath}")  # Log the location of saved screenshot
    
    return filepath
