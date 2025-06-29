import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

# ===== CONFIG =====
import os

resume_path = os.getenv("NAUKRI_RESUME")


email = os.getenv("NAUKRI_EMAIL")
password = os.getenv("NAUKRI_PASSWORD")


# ===== BROWSER SETUP =====
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# ===== START AUTOMATION =====
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
    print("✅ Logged in successfully.")

    time.sleep(5)
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    # ===== Try Resume Update Button (Main Section) =====
    try:
        update_resume_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Update resume")]')
            )
        )
        driver.execute_script("arguments[0].click();", update_resume_btn)
        print("🟡 Clicked main resume update button.")
    except:
        # ===== Fallback: Quick Links =====
        quicklink_update = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Update"))
        )
        driver.execute_script("arguments[0].click();", quicklink_update)
        print("🟢 Clicked sidebar resume update.")

    time.sleep(3)

    # ===== Find the hidden file input =====
    file_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    driver.execute_script("arguments[0].style.display = 'block';", file_input)
    print("📄 File input displayed:", file_input.is_displayed())

    # ===== Upload the file =====
    file_input.send_keys(resume_path)
    print("✅ Resume uploaded (file input triggered).")

    time.sleep(5)

except Exception as e:
    print("❌ Error:", str(e))

finally:
    # Optional: driver.quit()
    pass
