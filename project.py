import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api import verification_code
import os


def register_bot():
    # Set the path to your webdriver. For example, using Chrome:
    driver = webdriver.Edge()

    try:
        # Navigate to the online exchange website
        current_directory = os.getcwd()
        driver.get(f"file://{current_directory}/index.html")

        # Check if the registration is open by finding the element that indicates it
        try:
            start_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'نوبت دهی')]")
                )
            )
        except:
            print("Registration not open or element not found.")
            return

        # Check and accept the policies
        if check_and_accept_policies(driver):
            # Click the start button
            time.sleep(1)
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
                (By.ID, "acceptRules")
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
            EC.element_to_be_clickable((By.ID, "input-30"))
        )
        phone_input.send_keys("1234567890")  # Replace with the actual phone number

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        time.sleep(1)
        continue_button.click()

        global verification_code
        while not verification_code:
            time.sleep(5)
            verification_code = 1235

        # Now, send the verification code to your Flask API endpoint
        verify_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "verificationCode"))
        )
        verify_input.send_keys(verification_code)

        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='submit']")
            )  # Replace with the actual ID or other locator
        )
        time.sleep(1)
        verify_button.click()

    except:
        print("Unable to enter phone number or verify.")


# Schedule the bot to run every day at 8 p.m.
schedule.every().day.at("20:00").do(register_bot)
while True:
    schedule.run_pending()
    time.sleep(1)
