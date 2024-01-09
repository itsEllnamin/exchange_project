import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, jsonify
import requests


def register_bot():
    # Set the path to your webdriver. For example, using Chrome:
    driver_path = "/path/to/chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)

    try:
        # Navigate to the online exchange website
        driver.get("https://example.com")  # Replace with the actual URL

        # Check if the registration is open by finding the element that indicates it
        try:
            start_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.ID, "start-button")
                )  # Replace with the actual ID or other locator
            )
        except:
            print("Registration not open or element not found.")
            return

        # Check and accept the policies
        if check_and_accept_policies(driver):
            # Click the start button
            start_button.click()

            # Enter phone number and handle verification
            enter_phone_number(driver)

    finally:
        # Close the browser window
        driver.quit()


def check_and_accept_policies(driver):
    # Implement your logic to check and accept the policies here
    # For example, find the checkbox element and click it
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "policy-checkbox")
            )  # Replace with the actual ID or other locator
        )
        checkbox.click()
        return True
    except:
        print("Unable to check and accept policies.")
        return False


def enter_phone_number(driver):
    # Implement your logic to enter the phone number and handle verification here
    # For example, find the input field, enter the number, and click verify
    try:
        phone_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "phone-input")
            )  # Replace with the actual ID or other locator
        )
        phone_input.send_keys("1234567890")  # Replace with the actual phone number

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "continue-button")
            )  # Replace with the actual ID or other locator
        )
        continue_button.click()

        global verification_code
        while not verification_code:
            time.sleep(1)

        # Now, send the verification code to your Flask API endpoint
        verify_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "verify-input")
            )  # Replace with the actual ID or other locator
        )
        verify_input.send_keys(
            verification_code
        )  # Replace with the actual phone number

        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "verify-button")
            )  # Replace with the actual ID or other locator
        )
        verify_button.click()

    except:
        print("Unable to enter phone number or verify.")


# API
app = Flask(__name__)

verification_code = None

@app.route("/receive_code", methods=["POST"])
def receive_code():
    global verification_code
    verification_code = request.json.get("code")
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)


# Schedule the bot to run every day at 8 p.m.
schedule.every().day.at("20:00").do(register_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
