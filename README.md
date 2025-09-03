Automated Testing of E-commerce Web Application

Project Title:

Automated Testing of the Web Application – SauceDemo

Project Objective:

- The objective of this project is to automate the testing of the demo e-commerce web application, ensuring that core functionalities    like login, product selection, cart operations, sorting, checkout, and reset state work as expected.

- The automation framework simulates real-world user interactions such as:

    - Logging in with various types of users

    - Navigating the product catalog

    - Adding items to the cart

    - Performing checkout and validating order completion

    - Handling error scenarios with invalid credentials

    - Structured test scenarios validate functional correctness, UI behavior, and system responses under different conditions.


Scope:

- The automation framework is designed to:

- Simulate real-time user behavior for multiple user roles

- Validate functional workflows such as login, cart management, sorting, and checkout

- Randomly interact with product listings to mimic diverse purchase paths

- Ensure UI content correctness (e.g., product names, prices, order summary)

- Generate detailed execution reports with logs and screenshots


Preconditions:

- Both positive and negative test data will be included

- Data-driven and keyword-driven testing strategies will be followed

- Explicit waits will be used for handling dynamic web elements

- Tests will be designed with object-oriented programming principles

- Browser sessions will be closed properly after execution

Test Suite:

    Test-Case 1: Login with various predefined users

    Scenario: Login using different types of users (standard, locked-out, performance glitch, etc.)

    Expected Result: Each user’s access behavior should match system rules.

    Test-Case 2: Login with invalid credentials

    Scenario: Attempt login with incorrect username/password.

    Expected Result: Access should be denied.

    Test-Case 3: Validate logout functionality

    Scenario: Ensure logout button is available and functional.

    Expected Result: User should be redirected to login page after logout.

    Test-Case 4: Check cart icon visibility

    Scenario: Validate that the cart icon appears after login.

    Expected Result: Cart icon should always be accessible.

    Test-Case 5: Random selection of products and data extraction

    Scenario: Randomly pick 4 of the 6 products and fetch their names and prices.

    Expected Result: Selected product data should be logged/displayed correctly.

    Test-Case 6: Add selected products to cart and validate

    Scenario: Add 4 selected products to the cart and verify item count.

    Expected Result: Cart should show count = 4 and items listed correctly.

    Test-Case 7: Validate product details inside the cart

    Scenario: Navigate to cart and validate product names & prices.

    Expected Result: Cart details should match selected products.

    Test-Case 8: Complete checkout and validate order

    Scenario: Proceed to checkout, enter details, finalize order, and capture screenshot.

    Expected Result: Order summary and confirmation should display correct details.

    Test-Case 9: Validate sorting functionality on products page

    Scenario: Sort products by different criteria (e.g., price low→high, name Z→A).

    Expected Result: Product order should reflect correct sorting.

    Test-Case 10: Validate "Reset App State" functionality

    Scenario: Add products to cart, then reset app state.

    Expected Result: Cart and selections should reset to default state.


Technologies & Tools:

    Language: Python

    Framework: Selenium with PyTest

    Design Pattern: Page Object Model (POM)

    Reporting: HTML Reports, Allure Reports

    Logging: Python logging module (with file + console output)

    Test Data Management: JSON files

Project Structure:

ecommerce_automation/
│── reports/                # Test reports & screenshots
│── test_data/              # Test data files (JSON)
│── pages/                  # Page Object Model classes
│── tests/                  # Test scripts
│── utils/                  # Utility functions (logging, screenshots, reports)
│── conftest.py             # PyTest configuration
│── requirements.txt        # Dependencies
│── README.md               # Project documentation

How to Run Tests:

1 Clone the repository
git clone https://github.com/your-repo/ecommerce-automation.git
cd ecommerce-automation

2 Install dependencies
pip install -r requirements.txt

3 Run all tests with PyTest
pytest --html=report.html --self-contained-html

4 Run tests with Allure reporting
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

Reporting

- HTML Report → Auto-generated after execution

- Allure Report → Rich report with logs, screenshots, and test history

- Screenshots → Saved on failures in reports/screenshots/

Best Practices Followed

- Object-Oriented Principles for maintainability
- Exception Handling for resilience
- Dynamic waits for stability
- Code Comments & Logging for readability
- Reusable utilities & POM design