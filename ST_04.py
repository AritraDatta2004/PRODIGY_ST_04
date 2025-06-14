#Task 04
# Cross-Browser Login Test using BrowserStack (Selenium 4.33.0 Compatible)




import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Use your actual BrowserStack credentials here
BROWSERSTACK_USERNAME = "dattaaritra_bpZIht"
BROWSERSTACK_ACCESS_KEY = "pHVJrtWtbivovfvjwvcp"

URL = "https://hub-cloud.browserstack.com/wd/hub"

# List of browsers to test on
browsers = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "platformName": "Windows 11",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "userName": BROWSERSTACK_USERNAME,
            "accessKey": BROWSERSTACK_ACCESS_KEY,
            "buildName": "Task-04-Login-Test",
            "sessionName": "Chrome Login Test"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "platformName": "Windows 11",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "userName": BROWSERSTACK_USERNAME,
            "accessKey": BROWSERSTACK_ACCESS_KEY,
            "buildName": "Task-04-Login-Test",
            "sessionName": "Firefox Login Test"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "platformName": "OS X Monterey",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Monterey",
            "userName": BROWSERSTACK_USERNAME,
            "accessKey": BROWSERSTACK_ACCESS_KEY,
            "buildName": "Task-04-Login-Test",
            "sessionName": "Safari Login Test"
        }
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "platformName": "Windows 11",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "userName": BROWSERSTACK_USERNAME,
            "accessKey": BROWSERSTACK_ACCESS_KEY,
            "buildName": "Task-04-Login-Test",
            "sessionName": "Edge Login Test"
        }
    }
]

def run_test(capabilities):
    # Convert capabilities into a dictionary accepted by Selenium 4
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from selenium.webdriver.chrome.options import Options as ChromeOptions

    # Create the options object and add capabilities
    options = ChromeOptions()
    for key, value in capabilities.items():
        if key == "bstack:options":
            options.set_capability("bstack:options", value)
        else:
            options.set_capability(key, value)

    # Initialize remote driver with options only (Selenium 4.33.0 syntax)
    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    try:
        driver.get("http://the-internet.herokuapp.com/login")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )

        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )

        message = driver.find_element(By.ID, "flash").text
        assert "You logged into a secure area!" in message

        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Login successful!"}}')
        print(f"{capabilities['bstack:options']['sessionName']}: Login test passed.")

    except Exception as e:
        error_message = str(e).split("\n")[0]
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "' + error_message + '"}}')

    finally:
        driver.quit()

if __name__ == "__main__":
    for browser_cap in browsers:
        run_test(browser_cap)

