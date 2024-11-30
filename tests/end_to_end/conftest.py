import pytest
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def pause(seconds=2):
    import time
    time.sleep(seconds)

@pytest.fixture(scope='module')
def driver():
    options = webdriver.ChromeOptions()
    
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    # Navigate to the deployed app's URL
    deployed_app_url = "https://quizlytime.onrender.com/"
    driver.get(deployed_app_url)
    
    yield driver
    driver.quit()