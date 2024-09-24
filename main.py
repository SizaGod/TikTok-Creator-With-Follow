from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from selenium import webdriver

import string
from selenium.webdriver.common.keys import Keys

# Function to generate a random username
def generate_username():
    # Generate a random string of 8 characters consisting of lowercase letters
    return ''.join(random.choices(string.ascii_lowercase, k=8))

# Function to generate a random password
def generate_password():
    # Generate a random string of 10 characters consisting of letters (uppercase and lowercase) and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to generate a temporary email using YOPmail
def generate_temp_email(driver):
    try:
        # Open the YOPmail website
        driver.get("http://www.yopmail.com/en/")
        
        # Wait for the email input field to become clickable
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login")))
        
        # Generate random email address by appending '@yopmail.com' to the username
        email_address = generate_username() + "@yopmail.com"
        
        # Enter the email address and press Enter
        email_input.send_keys(email_address)
        email_input.send_keys(Keys.RETURN)

        return email_address
    
    except Exception as e:
        print("Failed to generate temporary email.")
        print(e)
        return None

# Function to create a TikTok account and follow a certain user
def create_account_and_follow(driver, user_profile_url):
    try:
        # Generate random username and password
        username = generate_username()
        password = generate_password()

        # Generate temporary email
        temp_email = generate_temp_email(driver)
        if temp_email is None:
            return

        print(f"Generated temporary email: {temp_email}")

        # Open TikTok in a new tab
        driver.execute_script("window.open('https://www.tiktok.com/signup', 'new_window')")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the policy checkbox to become clickable
        label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='signup-policy-all']")))
        label.click()

        # Locate and click on the "Next" button
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-e2e='next-button']")))
        next_button.click()

        print("Next button clicked successfully.")

        print("TikTok policy checkbox clicked successfully.")

        # Generate random month, day, and year
        random_month = str(random.randint(1, 12))
        random_day = str(random.randint(1, 28))
        random_year = str(random.randint(1987, 1998))

        # Select month
        month_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='birthdayMonth']")))
        month_options = month_dropdown.find_elements(By.TAG_NAME, "option")
        for option in month_options:
            if option.get_attribute("value") == random_month:
                option.click()
                break

        print("Month selected successfully.")

        # Select day
        day_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='birthdayDay']")))
        day_options = day_dropdown.find_elements(By.TAG_NAME, "option")
        for option in day_options:
            if option.get_attribute("value") == random_day:
                option.click()
                break

        print("Day selected successfully.")

        # Select year
        year_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='birthdayYear']")))
        year_options = year_dropdown.find_elements(By.TAG_NAME, "option")
        for option in year_options:
            if option.get_attribute("value") == random_year:
                option.click()
                break

        print("Year selected successfully.")

        # Wait for the email input field to become clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "email")))

        # Fill in registration form
        driver.find_element_by_name("email").send_keys(temp_email)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_name("username").send_keys(username)
        
        # Click on the sign-up button
        driver.find_element(By.CSS_SELECTOR, "button[class='jsx-526750592 btn btn-primary btn-lg']").click()

        # Wait for verification email (skipping this step for now)

        # Verify account and follow user
        driver.get(user_profile_url)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='follow']"))).click()

        print(f"Successfully created account {username} and followed user.")

    except Exception as e:
        print("An error occurred while creating the account.")
        print(e)

    finally:
        # Close the WebDriver instance
        driver.quit()

# URL of the TikTok user to follow
user_profile_url = "https://www.tiktok.com/@exampleuser"

try:
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Create account and follow user
    create_account_and_follow(driver, user_profile_url)

except Exception as e:
    print("An error occurred:", e)
