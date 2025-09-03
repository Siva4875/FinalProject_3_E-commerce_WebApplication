import json
from datetime import datetime

def generate_html_report(test_results, filename="test_report.html"):
    """Generate HTML test report with test results summary and details"""
    
    # HTML template with placeholders for dynamic test results
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Execution Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }
            .test { margin-bottom: 10px; padding: 10px; border-left: 5px solid; }
            .passed { border-color: #28a745; background-color: #d4edda; }
            .failed { border-color: #dc3545; background-color: #f8d7da; }
            .skipped { border-color: #ffc107; background-color: #fff3cd; }
            .screenshot { max-width: 100%; height: auto; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Test Execution Report</h1>
        
        <!-- Summary section -->
        <div class="summary">
            <h2>Summary</h2>
            <p>Total Tests: {total_tests}</p>
            <p>Passed: {passed}</p>
            <p>Failed: {failed}</p>
            <p>Skipped: {skipped}</p>
            <p>Execution Time: {execution_time}</p>
        </div>
        
        <!-- Detailed results -->
        <h2>Test Details</h2>
        {test_details}
    </body>
    </html>
    """
    
    # -------------------------
    # Calculate summary counts
    # -------------------------
    total_tests = len(test_results)  # Total number of executed tests
    passed = sum(1 for result in test_results if result['status'] == 'passed')
    failed = sum(1 for result in test_results if result['status'] == 'failed')
    skipped = sum(1 for result in test_results if result['status'] == 'skipped')
    
    # -------------------------
    # Build detailed test results
    # -------------------------
    test_details = ""
    for result in test_results:
        status_class = result['status']  # CSS class for test status (passed/failed/skipped)
        
        # Add test block with name, status, and duration
        test_details += f"""
        <div class="test {status_class}">
            <h3>{result['name']}</h3>
            <p>Status: <strong>{result['status']}</strong></p>
            <p>Duration: {result['duration']} seconds</p>
        """
        
        # Add screenshot link if available
        if result.get('screenshot'):
            test_details += f"""
            <p>Screenshot: <a href="{result['screenshot']}" target="_blank">View Screenshot</a></p>
            """
        
        # Add error message if available
        if result.get('error'):
            test_details += f"""
            <p>Error: {result['error']}</p>
            """
        
        # Close test block div
        test_details += "</div>"
    
    # -------------------------
    # Fill template with data
    # -------------------------
    html_content = html_template.format(
        total_tests=total_tests,
        passed=passed,
        failed=failed,
        skipped=skipped,
        execution_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
        test_details=test_details
    )
    
    # -------------------------
    # Save report to HTML file
    # -------------------------
    with open(filename, 'w') as f:
        f.write(html_content)
    
    # Return filename for reference
    return filename
