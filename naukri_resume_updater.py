import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables
load_dotenv()

email = os.getenv("NAUKRI_EMAIL")
password = os.getenv("NAUKRI_PASSWORD")
resume_path = os.getenv("NAUKRI_RESUME_URL")

# Headless Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://www.naukri.com/")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@placeholder="Enter your active Email ID / Username"]')
        )
    ).send_keys(email)

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//button[contains(text(), "Continue") or contains(text(), "Login") or contains(text(), "Next")]',
            )
        )
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@placeholder="Enter your password"]')
        )
    ).send_keys(password)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Login")]'))
    ).click()
    print("✅ Logged in successfully")

    time.sleep(5)
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    try:
        update_resume_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Update resume")]')
            )
        )
        driver.execute_script("arguments[0].click();", update_resume_btn)
        print("🟡 Clicked main resume update button.")
    except:
        quicklink_update = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Update"))
        )
        driver.execute_script("arguments[0].click();", quicklink_update)
        print("🟢 Clicked sidebar resume update.")

    time.sleep(3)

    file_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    driver.execute_script("arguments[0].style.display = 'block';", file_input)
    file_input.send_keys(resume_path)
    print("✅ Resume uploaded")

    time.sleep(5)

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()
