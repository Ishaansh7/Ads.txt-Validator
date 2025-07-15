from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 🔧 Path to your ChromeDriver
chromedriver_path = r"C:\Users\Ishaan Sharma\Desktop\code\chromedriver-win64\chromedriver.exe"

# 🔧 Download directory
download_dir = r"C:\Users\Ishaan Sharma\Downloads"

# 🔐 Credentials
email = "dops@vdo.ai"
password = "VDO@AI2025"

# ✅ Chrome options
options = Options()
options.add_argument("--start-maximized")
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)

# ✅ Launch Chrome
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    # 🌐 Step 1: Go to login page
    driver.get("https://analytics.highr.ai")

    # 🕐 Wait for login form
    wait.until(EC.presence_of_element_located((By.NAME, "email")))

    # ✍️ Step 2: Fill login details
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)

    # 🔘 Click login button
    login_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.mat-focus-indicator.new-auth-button")
    ))
    login_button.click()
    print("🔓 Logged in!")

    # 🧭 Step 3: Click the Analytics tile by its image
    analytics_tile = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "img[src*='analytics.svg']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", analytics_tile)
    time.sleep(1)
    analytics_tile.click()
    print("📊 Opened Analytics dashboard")

    # 🧭 Step 3.5: Switch to new tab if opened
    original_window = driver.current_window_handle
    all_windows = driver.window_handles
    for handle in all_windows:
        if handle != original_window:
            driver.switch_to.window(handle)
            print("🪟 Switched to new tab")
            break

    # ⏳ Step 4: Wait for dashboard to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.excel-icon")))

    # 🧩 Step 5: Select from dropdown
    print("📂 Selecting dropdown option...")
    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mat-select-4")))
    dropdown.click()

    # Wait for option 9 to be clickable, then click
    option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mat-option-9")))
    option.click()
    print("✅ Selected option from dropdown")

    # ⏳ Step 5.5: Wait for overlay to disappear
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
        print("✅ Overlay dismissed")
    except:
        print("⚠️ Overlay did not disappear in time")

    # 📥 Step 6: Click Excel download button
    print("📥 Locating Excel download button...")
    download_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.excel-icon a")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_link)
    time.sleep(1)

    # Capture list of files before clicking
    files_before = set(os.listdir(download_dir))

    download_link.click()
    print("✅ Excel download triggered!")

    # 🕙 Step 7: Wait for new file to appear
    time.sleep(6)
    files_after = set(os.listdir(download_dir))
    new_files = files_after - files_before
    downloaded = [f for f in new_files if f.endswith(('.csv', '.xlsx'))]

    if downloaded:
        print(f"✅ Download completed: {downloaded}")
    else:
        print("❌ No file downloaded.")

finally:
    driver.quit()
    print("✅ Done and browser closed.")
