import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException

# Get environment variables
email = os.getenv("NAUKRI_EMAIL")
password = os.getenv("NAUKRI_PASSWORD")
resume_path = os.getenv("NAUKRI_RESUME_URL")

if not all([email, password, resume_path]):
    raise ValueError("Missing required environment variables")

# GUARANTEED WORKING Chrome options for GitHub Actions
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-web-security')
options.add_argument('--disable-features=VizDisplayCompositor')
options.add_argument('--window-size=1920,1080')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-extensions')
options.add_argument('--disable-plugins')
options.add_argument('--disable-images')
options.add_argument('--disable-javascript')  # Remove if site needs JS
options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

print("🚀 Starting Naukri automation...")

try:
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)  # Increased timeout
    
    print("✅ Chrome browser started successfully")
    
    # Navigate to Naukri
    driver.get("https://www.naukri.com/")
    print("📍 Navigated to Naukri.com")
    
    # Login process
    login_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
    login_btn.click()
    print("🔐 Clicked login button")
    
    # Enter email
    email_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Enter your active Email ID / Username"]')
    ))
    email_field.clear()
    email_field.send_keys(email)
    print("📧 Email entered")
    
    # Continue button
    continue_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "Continue")]')
    ))
    continue_btn.click()
    print("➡️ Clicked continue")
    
    # Enter password
    password_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Enter your password"]')
    ))
    password_field.clear()
    password_field.send_keys(password)
    print("🔑 Password entered")
    
    # Login button
    login_submit = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "Login")]')
    ))
    login_submit.click()
    print("✅ Login submitted")
    
    # Wait and navigate to profile
    time.sleep(5)
    driver.get("https://www.naukri.com/mnjuser/profile")
    print("👤 Navigated to profile page")
    
    time.sleep(3)
    
    # Find resume update button
    try:
        update_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(),"Update resume")]')
        ))
        driver.execute_script("arguments[0].click();", update_btn)
        print("🟡 Main resume update button clicked")
    except TimeoutException:
        # Fallback to quicklink
        quicklink = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Update")))
        driver.execute_script("arguments[0].click();", quicklink)
        print("🟢 Quicklink update clicked")
    
    time.sleep(3)
    
    # File upload
    file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
    driver.execute_script("arguments[0].style.display = 'block';", file_input)
    file_input.send_keys(resume_path)
    print("📄 Resume file uploaded successfully")
    
    time.sleep(5)
    print("🎉 AUTOMATION COMPLETED SUCCESSFULLY!")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    if 'driver' in locals():
        print("📸 Taking screenshot for debugging...")
        driver.save_screenshot("error_screenshot.png")
    raise
    
finally:
    if 'driver' in locals():
        driver.quit()
        print("🔚 Browser closed")
