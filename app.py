from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, random, json
import dotenv, os
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.linkedin.com')
driver.delete_all_cookies()

expected_samesite_values = ["Strict", "Lax", "None"]

with open("cookies.json", "r") as file:
    cookies = json.load(file)
    for cookie in cookies:
        if cookie.get("sameSite") not in expected_samesite_values:
            cookie["sameSite"] = "None"
    for cookie in cookies:
        driver.add_cookie(cookie)
file = open('data.txt', 'a')
def visit_and_operate(url,pages=1):
    url = url + f"&page={pages}"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    while True:
        pages += 1
        file.write(f"Page {pages}\n")
        time.sleep(random.randint(5, 10))
        buttons = driver.find_elements(By.CSS_SELECTOR, 'div.entry-point.profile-action-compose-option')
        for button in buttons:
            button.click()
            time.sleep(random.randint(2, 5))  
            link = driver.find_element(By.CSS_SELECTOR, 'a.app-aware-link[target="_blank"]')
            if link.get_attribute('href') == "https://www.linkedin.com/help/linkedin/answer/139":
                title = driver.find_element(By.CSS_SELECTOR, 'div.artdeco-entity-lockup__title')
                subtitle = driver.find_element(By.CSS_SELECTOR, 'div.artdeco-entity-lockup__subtitle')
                file.write(f"{title.text} - {subtitle.text}\n")
            time.sleep(random.randint(1, 3))
            close_button = driver.find_element(By.CSS_SELECTOR, 'use[href="#close-small"]')
            close_button.click()
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next"]')))
            next_button.click()
        except Exception as e:
            print(f"Couldn't navigate to the next page: {e}")
            break
        file.flush()

dotenv.load_dotenv()
URL = os.getenv("LINKEDIN_URL")
visit_and_operate(URL)
driver.quit()
file.close()
