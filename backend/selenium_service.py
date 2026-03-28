import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service  = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://semakmule.rmp.gov.my/")
time.sleep(10)

driver.quit()