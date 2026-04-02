import os
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed

executor = ThreadPoolExecutor(max_workers=2)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(BASE_DIR, "chromedriver.exe")

service  = Service(executable_path=driver_path)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://semakmule.rmp.gov.my/")

def check_email(email):
    return None
def check_phone_number(number):

    dropdown_element = __get_element(By.XPATH, "//div[contains(@role, 'combobox')]")
    __click_element(dropdown_element)

    choose_phone_element = __get_element(By.XPATH, "//li[contains(@data-value, 'telefon')]")
    __click_element(choose_phone_element)

    input_element = __get_element(By.XPATH, "//input[contains(@placeholder, 'Masukkan No Telefon')]")
    __safe_input(number, input_element)

    semak_button = __get_element(By.XPATH, "//button[contains(text(), 'Semak')]")
    __click_element(semak_button)

    result = __get_result(number)

    close_button = __get_element(By.XPATH, "//button[img[@class='ReportCheckDialog_closeIcon__WvekQ']] ")
    __click_element(close_button)


    if result is None:
        print("No result found on " + number)
        return {
            "scam" : False
        }
    else:
        print("Result found on " + number + " with " + result + " report")
        return {
            "scam" : True,
            "report_count" : result
        }


def __safe_input(text, element):
    while element.get_attribute("value").strip() == "":
        element.send_keys("Dummy Value")

    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACKSPACE)

    element.send_keys(text)

def __get_element(by, path):
    try:
        return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, path)))
    except TimeoutException:
        return None

def __click_element(element):
    element.click()

def __get_result(key):
    resultPath = "//tr[td[1][text() = '{}']]".format(key)
    noResultPath = "//p[contains(text(), 'Tiada Rekod Ditemui')]"
    RESULT = "result"
    RESULTNOTFOUND = "resultnotfound"

    future_to_task = {
        executor.submit(__get_element, By.XPATH, resultPath): RESULT,
        executor.submit(__get_element, By.XPATH, noResultPath): RESULTNOTFOUND
    }

    for future in as_completed(future_to_task):
        task_name = future_to_task[future]
        result = future.result()
        if task_name == RESULTNOTFOUND and result is not None:
            return None
        else:
            return  result.find_element(By.XPATH, "./td[2]").text

if __name__ == "__main__":
    check_phone_number("1111")
    check_phone_number("1234")
