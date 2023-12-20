from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from log import config_logger
logger = config_logger()

from selenium.common.exceptions import NoSuchElementException, TimeoutException


def login():
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