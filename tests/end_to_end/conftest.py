# import pytest
# from threading import Thread
# from subprocess import Popen
# import time

# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# from app import create_app

# def pause(seconds=2):
#     time.sleep(seconds)

# @pytest.fixture(scope='module')
# def driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--enable-logging")
#     options.add_argument("--v=1")
    
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--ignore-ssl-errors')

#     service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.implicitly_wait(10) 
#     yield driver
#     driver.quit()

# @pytest.fixture(scope='module')
# def server():
#     app = create_app()
#     app_thread = Thread(
#         target=app.run,
#         kwargs={'port': 5000, 'debug': False, 'use_reloader': False}
#     )
#     app_thread.daemon = True
#     app_thread.start()
#     pause(10) # give time for server to start
#     yield 

# @pytest.fixture(scope='module')
# def client():
#     client_process = Popen(['npm', 'run', 'dev'], cwd='views')
#     pause(5)  # give time for client to start
#     yield 
#     client_process.terminate()


# @pytest.fixture(scope='module')
# def setup_app(server, client):
#     # ensures server and client are running before running tests
#     yield


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

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    # Navigate to the deployed app's URL
    deployed_app_url = "https://quizlytime.onrender.com/"
    driver.get(deployed_app_url)
    
    yield driver
    driver.quit()