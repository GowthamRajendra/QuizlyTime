import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

unique_email = f"user-{time.time()}@test.com"

def pause(seconds=2):
    time.sleep(seconds)

def test_register(driver):
    driver.get("https://quizlytime.onrender.com/register")
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "formUsername").send_keys("testUser")
    driver.find_element(By.ID, "formEmail").send_keys(unique_email)
    driver.find_element(By.ID, "formPassword").send_keys("password")
    pause(2)
    driver.find_element(By.ID, "registerButton").click()

    for request in driver.requests:
        if request.response:
            if "/register" in request.url and request.method == "POST":
                assert request.response.status_code == 201
                assert request.response.body == b'{"message":"User created successfully."}'
                break
    else:
        assert False, "Request not found"


def test_login(driver):
    driver.get("https://quizlytime.onrender.com/login")
    driver.find_element(By.ID, "formEmail").send_keys(unique_email)
    driver.find_element(By.ID, "formPassword").send_keys("password")
    pause(2)
    driver.find_element(By.ID, "loginButton").click()

    for request in driver.requests:
        if request.response:
            if "/login" in request.url and request.method == "POST":
                assert request.response.status_code == 200
                assert request.response.body == b'{"message":"Login successful."}'
                break   
    else:
        assert False, "Request not found"

