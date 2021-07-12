import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def create_driver_Session() -> WebDriver:
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # driver.maximize_window()
    return driver


def eleID(eleid, driver: WebDriver, tout=10) -> WebElement:
    wait = WebDriverWait(driver, tout)
    wait.until(ec.presence_of_element_located((By.ID, eleid)))
    wait.until(ec.visibility_of_element_located((By.ID, eleid)))
    return driver.find_element_by_id(eleid)


def eleXpath(xpath: str, driver, tout=10) -> WebElement:
    wait = WebDriverWait(driver, tout)
    wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
    wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
    return driver.find_element_by_xpath(xpath)


def if_present(xpath, driver: WebDriver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def if_present_id(id, driver: WebDriver):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True


def try_catch(fun):
    try:
        fun()
    except Exception as exc:
        print(exc)


def store_student_id_password(data: dict):
    with open("studentData.json", "w") as write_file:
        json.dump(data, write_file)


def read_json(path):
    with open(path, "r") as read_file:
        return json.load(read_file)


def update_json(path, updated_data):
    with open(path, "r+") as file:
        data: dict = json.load(file)
        data.update(updated_data)
        file.seek(0)
        json.dump(data, file)
