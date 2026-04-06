import os
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
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
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://semakmule.rmp.gov.my/")

ACCOUNT_NO = "bank"
PHONE_NUMBER = "telefon"
COMPANY_NAME = "namasyarikat"

def check_company_name(company_name):
    print("Checking company name: " + company_name)
    __do_check(company_name, COMPANY_NAME)
    return __get_result_for_company_name()

def check_account_no(account_no):
    print("Checking account number: " + account_no)
    __do_check(account_no, ACCOUNT_NO)
    return __get_result()

def check_phone_number(number):
    print("Checking phone number: " + number)
    __do_check(number, PHONE_NUMBER)
    return __get_result()


def __do_check(data, check_type):

    dropdown_element = __get_element(By.XPATH, "//div[contains(@role, 'combobox')]")
    __click_element(dropdown_element)

    choose_phone_element = __get_element(By.XPATH, "//li[contains(@data-value,'" + check_type + "')]")
    __click_element(choose_phone_element)

    input_element = __get_element(By.XPATH, "//*[@id=':r5:']")
    __safe_input(data, input_element)

    semak_button = __get_element(By.XPATH, "//button[contains(text(), 'Semak')]")
    __click_element(semak_button)


def __safe_input(text, element):

    while element.get_attribute("value").strip() == "":
        element.send_keys("Dummy Value")

    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACKSPACE)

    element.send_keys(text)

def __get_element(by, path):
    try:
        return WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((by, path)))
    except TimeoutException:
        return None

def __click_element(element):
    element.click()

def __get_result():
    resultPath = "//table[@class = 'ReportCheckDialog_table__qou1V']/tbody[1]/tr[1]"
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

            close_button = __get_element(By.XPATH, "//button[img[@class='ReportCheckDialog_closeIcon__WvekQ']] ")
            __click_element(close_button)
            print("No result found")
            return {
                "scam": False
            }
        else:
            number = result.find_element(By.XPATH, "./td[1]").text
            count = result.find_element(By.XPATH, "./td[2]").text

            close_button = __get_element(By.XPATH, "//button[img[@class='ReportCheckDialog_closeIcon__WvekQ']] ")
            __click_element(close_button)

            print(count + " reports")

            return {
                "scam": True,
                "number": number,
                "count": count
            }

def __get_result_for_company_name():
    resultPath = "//table[@class = 'ReportCheckDialog_table__qou1V']/tbody[1]"
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

            close_button = __get_element(By.XPATH, "//button[img[@class='ReportCheckDialog_closeIcon__WvekQ']] ")
            __click_element(close_button)
            print("No result found")
            return {
                "scam": False
            }
        else:
            data = []

            try:
                index = 1
                while True:
                    company_name = result.find_element(By.XPATH, f"./tr[{index}]/td[3]").text
                    data.append(company_name)
                    index += 1

            except NoSuchElementException:
                print("Finish fetching result")

            print("Result: ")
            print(data)
            close_button = __get_element(By.XPATH, "//button[img[@class='ReportCheckDialog_closeIcon__WvekQ']] ")
            __click_element(close_button)

            return {
                "scam": True,
                "result": data
            }

if __name__ == "__main__":
    check_phone_number("1111")
    check_phone_number("1234")
    check_account_no("1234")
    check_account_no("1111")
    check_company_name("nestle")
    check_company_name("cvc")
