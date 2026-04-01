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

service  = Service(executable_path="chromedriver.exe")
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options = chrome_options)

def check_phone_number(number):
    driver.get("https://semakmule.rmp.gov.my/")

    dropdown_element = getElement(By.XPATH, "//div[contains(text(), 'No Akaun Bank')]")
    clickElement(dropdown_element)

    choose_phone_element = getElement(By.XPATH, "//li[contains(@data-value, 'telefon')]")
    clickElement(choose_phone_element)

    input_element = getElement(By.XPATH, "//input[contains(@placeholder, 'Masukkan No Telefon')]")
    safeInput(number, input_element)

    semak_button = getElement(By.XPATH, "//button[contains(text(), 'Semak')]")
    clickElement(semak_button)

    result = getResult(number)

    if result is None:
        print("No result")
    else:
        print("Result found on " + number)

    time.sleep(10)
    driver.quit()

def safeInput(text, element):
    while element.get_attribute("value").strip() == "":
        element.send_keys("Dummy Value")

    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACKSPACE)

    element.send_keys(text)

def getElement(by, path):
    try:
        return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, path)))
    except TimeoutException:
        return None

def clickElement(element):
    time.sleep(0.5)
    element.click()

def getResult(key):
    resultPath = "//tr[td[1][text() = '{}']]".format(key)
    noResultPath = "//p[contains(text(), 'Tiada Rekod Ditemui')]"
    RESULT = "result"
    RESULTNOTFOUND = "resultnotfound"

    #Run 2 get element at the same time
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_task = {
            executor.submit(getElement, By.XPATH,resultPath): RESULT,
            executor.submit(getElement,By.XPATH, noResultPath): RESULTNOTFOUND
        }

        for future in as_completed(future_to_task):
            task_name = future_to_task[future]
            result = future.result()




    return


if __name__ == "__main__":
    check_phone_number("1234")
