import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

unique_email = f"user-{time.time()}@test.com"
WEBSITE_URL = "http://localhost:5173"

def pause(seconds=2):
    time.sleep(seconds)

def test_register(driver):
    driver.get(WEBSITE_URL)
    pause(5)
    driver.find_element(By.LINK_TEXT, "Register").click()
    pause(5)
    driver.find_element(By.ID, "formUsername").send_keys("testUser")
    driver.find_element(By.ID, "formEmail").send_keys(unique_email)
    driver.find_element(By.ID, "formPassword").send_keys("password")
    pause(2)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    pause(2)
    for request in driver.requests:
        if request.response:
            print(request.response)

            if "/register" in request.url and request.method == "POST":
                assert request.response.status_code == 201
                # assert request.response.json["message"] == "User created successfully."
                break

def test_login(driver):
    pause(5)
    driver.get(WEBSITE_URL)
    pause(5)
    driver.find_element(By.LINK_TEXT, "Login").click()
    driver.find_element(By.ID, "formEmail").send_keys(unique_email)
    driver.find_element(By.ID, "formPassword").send_keys("password")
    pause(2)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    pause(2)

    for request in driver.requests:
        if request.response:
            print(request.response)
            
            if "/login" in request.url and request.method == "POST":
                assert request.response.status_code == 200
                # assert request.response.json["message"] == "Login successful."
                break   

def test_logout(driver):
    pause(5)
    driver.get(WEBSITE_URL)
    pause(5)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    pause(2)
    for request in driver.requests:
        if request.response:
            print(request.response)
            
            if "/logout" in request.url and request.method == "POST":
                assert request.response.status_code == 200
                # assert request.response.json["message"] == "Logout successful."
                break

