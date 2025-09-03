import json
import os

def get_users():
    """
    Reads the users.json file from the 'test_data' directory and returns its contents.
    Used for fetching predefined users (username & password) for login tests.
    """
    # Build the absolute path to users.json file (two directories up -> test_data folder)
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", "users.json")
    
    # Open the file and load its contents as a Python object (list/dict depending on JSON structure)
    with open(file_path, 'r') as file:
        return json.load(file)


def get_test_data():
    """
    Reads the test_data.json file from the 'test_data' directory and returns its contents.
    Used for fetching generic test data (like product selections, expected values, etc.).
    """
    # Build the absolute path to test_data.json file (two directories up -> test_data folder)
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", "test_data.json")
    
    # Open the file and load its contents as a Python object (list/dict depending on JSON structure)
    with open(file_path, 'r') as file:
        return json.load(file)
