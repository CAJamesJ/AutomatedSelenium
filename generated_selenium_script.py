from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Edge()
driver.maximize_window()
driver.get('https://dev.sorrl.mcss.gov.on.ca/SORRL/public/login.xhtml')  # Replace with your target URL
wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.ID, "details-button"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "proceed-link"))).click()
time.sleep(1)
wait.until(EC.presence_of_element_located((By.ID, "loginForm:loginName"))).send_keys("dafrahouhexei-3042@yopmail.com")
wait.until(EC.presence_of_element_located((By.ID, "loginForm:inputPassword"))).send_keys("aA1!aA1!aA1!aA1!")
wait.until(EC.element_to_be_clickable((By.ID, "loginForm:login"))).click()
time.sleep(1000)
driver.quit()