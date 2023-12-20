from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re

from log import config_logger
logger = config_logger()

from sophia_login import sophia_login

driver = sophia_login()

    # start looping through the records.
df = pd.read_csv('update_status.csv')
urls = df['Invention Edit URL']
# print(urls)

for url in urls:
    try:
        logger.info(url)
        driver.implicitly_wait(10)
            # start looping through the pages to trigger a push
        driver.get(url)
        driver.maximize_window()
        logger.info(f'arrived: {url}')


        disclosure_status_dropdown = driver.find_element(By.XPATH, '//*[@id="oform:: 4"]')
        disclosure_status_dropdown = Select(disclosure_status_dropdown)
        disclosure_status_dropdown.select_by_visible_text('Stage 5 - Marketing')

        save_details_button = driver.find_element(By.CLASS_NAME, 'standard_button')
        save_details_button.click()

        # Wait for the URL to change to the detail page
        # form = https://umn.wellspringsoftware.net/kms/invention/form/5670/
        # detail = https://umn.wellspringsoftware.net/kms/invention/detail/5670
        new_url = url.replace('form','detail')
        new_url = new_url[:-1]   
        WebDriverWait(driver, 8).until(EC.url_to_be(new_url))
        logger.info(f'Done: {new_url}')
    
    except NoSuchElementException as e:
        logger.error(f'Element not found on {url}: {e}')
    except TimeoutException as e:
        logger.error(f"Timed out waiting for URL change on {url}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred on {url}: {e}")
