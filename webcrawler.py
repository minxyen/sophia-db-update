from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from log import config_logger
logger = config_logger()

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import re

    # driver configuration
options = webdriver.ChromeOptions()
user_data_dir = r"C:/Users/Hsieh149/AppData/Local/Google/Chrome/User Data"
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument("profile-directory=Default")
options.add_experimental_option('detach', True)

    # login to Sophia, to the example contact page.
driver = webdriver.Chrome(options = options)
driver.get('https://umn.wellspringsoftware.net/kms/person/form/33641/')
driver.implicitly_wait(10)
login = driver.find_element(By.LINK_TEXT, 'Login using UMN credentials')
login.click()
driver.implicitly_wait(10)
signin = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[3]/button')
signin.click()
time.sleep(8)


    # start looping through the records.
df = pd.read_excel('contact-selenium02.xlsx')
person_ids = df['person_id']

for person_id in person_ids:
    try:
        url = f'https://umn.wellspringsoftware.net/kms/person/form/{person_id}'
        logger.info(url)
        driver.implicitly_wait(10)
            # start looping through the pages to trigger a push
        driver.get(url)
        driver.maximize_window()
        logger.info(f'arrived EDIT PAGE: {person_id}')
        standard_button = driver.find_element(By.CLASS_NAME, 'standard_button')
        standard_button.click()

        # Wait for the URL to change to the detail page
        new_url = f'https://umn.wellspringsoftware.net/kms/person/detail/{person_id}'
        WebDriverWait(driver, 5).until(EC.url_to_be(new_url))

        # Find the element  # need to fix this.
        salesforce_contact_id_element = driver.find_element(By.XPATH, '//*[@id="datarow_salesforce_contact_id"]/td')

        # Check if the text content is a valid 18-digit ID using a regular expression
        if len(salesforce_contact_id_element.text.strip()) != 18:
            raise ValueError("Salesforce contact ID does not have exactly 18 characters")
    
        logger.info(f'push triggered: {person_id} to {salesforce_contact_id_element.text}')

    except NoSuchElementException as e:
        logger.error(f'Element not found on {url}: {e}')
    except TimeoutException as e:
        logger.error(f"Timed out waiting for URL change on {url}: {e}")
    except ValueError as e:
        logger.error(f"Salesforce contact ID is 'None' on {url}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred on {url}: {e}")

