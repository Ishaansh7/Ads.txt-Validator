from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

# Configuration
chromedriver_path = r"C:\Users\Ishaan Sharma\Desktop\code\chromedriver-win64\chromedriver.exe"
download_dir = r"C:\Users\Ishaan Sharma\Downloads"
email = "dops@vdo.ai"
password = "VDO@AI2025"

# Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False  # Important for downloads
}
options.add_experimental_option("prefs", prefs)

# Launch Chrome
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

def zoom_out_to_80_percent(driver):
    """Zoom out to 80% to make download button visible"""
    try:
        # Method 1: JavaScript zoom (most reliable)
        driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(2)
        print("✅ Zoomed out to 80% using JavaScript")
        
        # Alternative Method 2: Keyboard shortcut (backup)
        # body = driver.find_element(By.TAG_NAME, "body")
        # for i in range(3):  # Zoom out 3 times
        #     body.send_keys(Keys.CONTROL + "-")
        #     time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ Error zooming out: {e}")
        # Try keyboard method as fallback
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            for i in range(3):
                body.send_keys(Keys.CONTROL + "-")
                time.sleep(0.5)
            print("✅ Zoomed out using keyboard shortcuts")
        except Exception as e2:
            print(f"❌ Both zoom methods failed: {e2}")

def find_download_button_comprehensive(driver):
    """Comprehensive search for download button"""
    print("🔍 Searching for download button comprehensively...")
    
    # Extended list of selectors based on common patterns
    selectors_to_try = [
        # Your original selectors
        "//div[contains(@class, 'excel-icon')]//img",
        "//div[contains(@class, 'excel-icon')]",
        "//img[contains(@src, 'excel')]",
        "//*[contains(@aria-label, 'download')]",
        "//button[contains(@class, 'export-btn')]",
        
        # Additional comprehensive selectors
        "//button[contains(@class, 'download')]",
        "//button[contains(@class, 'export')]",
        "//button[contains(@class, 'csv')]",
        "//button[contains(text(), 'Download')]",
        "//button[contains(text(), 'Export')]",
        "//button[contains(text(), 'CSV')]",
        "//button[contains(text(), 'Excel')]",
        "//a[contains(@class, 'download')]",
        "//a[contains(@class, 'export')]",
        "//i[contains(@class, 'download')]/..",
        "//i[contains(@class, 'export')]/..",
        "//i[contains(@class, 'fa-download')]/..",
        "//i[contains(@class, 'fa-file-excel')]/..",
        "//span[contains(@class, 'download')]/..",
        "//span[contains(@class, 'export')]/..",
        "*[contains(@title, 'Download')]",
        "*[contains(@title, 'Export')]",
        "*[contains(@title, 'CSV')]",
        "*[contains(@title, 'Excel')]",
        
        # Look in specific areas
        "//div[contains(@class, 'toolbar')]//button",
        "//div[contains(@class, 'header')]//button",
        "//div[contains(@class, 'actions')]//button",
        "//div[contains(@class, 'controls')]//button",
        
        # Look near the table/data section
        "//div[contains(text(), 'Date, Sites')]/..//button",
        "//div[contains(text(), 'Date, Sites')]/..//a",
        "//div[contains(text(), 'Date, Sites')]/..//i/..",
        
        # Generic clickable elements that might be styled as download buttons
        "//div[@role='button' and @tabindex='0']",
        "//span[@role='button']",
    ]
    
    found_button = None
    
    for selector in selectors_to_try:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            for element in elements:
                if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                    found_button = element
                    print(f"✅ Found download button with selector: {selector}")
                    return found_button
        except Exception as e:
            continue
    
    return found_button

def scroll_and_search_download_button(driver):
    """Scroll through the page to find download button"""
    print("🔄 Scrolling to find download button...")
    
    # Try scrolling to different sections
    scroll_targets = [
        "//div[contains(@class, 'dashboard')]",
        "//div[contains(@class, 'content')]",
        "//div[contains(@class, 'main')]",
        "//div[contains(text(), 'Date, Sites')]",
        "body"
    ]
    
    for target in scroll_targets:
        try:
            element = driver.find_element(By.XPATH, target)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            
            # Try to find download button after scrolling
            button = find_download_button_comprehensive(driver)
            if button:
                return button
                
        except Exception as e:
            continue
    
    # Try scrolling to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    return find_download_button_comprehensive(driver)

try:
    # Step 1: Login
    print("🌐 Navigating to dashboard...")
    driver.get("https://analytics.highr.ai/dashboard")
    
    print("🔑 Logging in...")
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.mat-focus-indicator.new-auth-button")
    )).click()
    print("✅ Login successful!")

    # Step 2: Navigate to Analytics
    print("📊 Opening Analytics dashboard...")
    analytics_tile = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//img[contains(@src, 'analytics.svg')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", analytics_tile)
    analytics_tile.click()
    
    # Wait for dashboard to load
    print("⏳ Waiting for dashboard to load...")
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'dashboard-container') or contains(@class, 'card-siemer')]"))
    )
    
    # Wait specifically for the "Date, Sites" section to load
    print("⏳ Waiting for Date, Sites section to load...")
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Date, Sites')]")))
        print("✅ Date, Sites section loaded!")
    except Exception as e:
        print(f"⚠️ Could not find Date, Sites section: {e}")
    
    time.sleep(3)  # Additional buffer time

    # Step 3: ZOOM OUT TO 80%
    print("🔍 Zooming out to 80% to make download button visible...")
    zoom_out_to_80_percent(driver)
    
    # Scroll to the Date, Sites section
    print("📜 Scrolling to Date, Sites section...")
    try:
        date_sites_section = driver.find_element(By.XPATH, "//div[contains(text(), 'Date, Sites')]")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", date_sites_section)
        time.sleep(2)
        print("✅ Scrolled to Date, Sites section!")
    except Exception as e:
        print(f"⚠️ Could not scroll to Date, Sites section: {e}")
        # Try scrolling to bottom as fallback
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Step 4: Find and click Excel icon using exact selectors
    print("🔍 Locating Excel download button using exact selectors...")
    
    # Use the exact selectors you provided
    exact_selectors = [
        # XPath you provided
        "/html/body/app-root/app-home/div/div/div/div/div[2]/app-dashboard/div/div[3]/div[3]/div[1]/div[2]/a/img",
        # CSS selector you provided
        "body > app-root > app-home > div > div > div > div > div.main_layout_side_container > app-dashboard > div > div.show.ng-star-inserted > div.new-dashboard-card > div.list-top-section > div.excel-icon > a > img",
        # More flexible versions
        "//div[contains(@class, 'excel-icon')]//a//img",
        "//div[contains(@class, 'excel-icon')]//a",
        "//div[contains(@class, 'list-top-section')]//div[contains(@class, 'excel-icon')]//a",
        ".excel-icon a img",
        ".excel-icon a",
        ".list-top-section .excel-icon a img"
    ]
    
    excel_icon = None
    
    for i, selector in enumerate(exact_selectors):
        try:
            print(f"🔍 Trying selector {i+1}: {selector[:50]}...")
            
            if selector.startswith("//") or selector.startswith("/html"):
                # XPath selector
                elements = driver.find_elements(By.XPATH, selector)
            else:
                # CSS selector
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for element in elements:
                if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                    excel_icon = element
                    print(f"✅ Found download button with selector {i+1}!")
                    break
            
            if excel_icon:
                break
                
        except Exception as e:
            print(f"❌ Selector {i+1} failed: {e}")
            continue

    if excel_icon:
        print("🖱️ Attempting to download...")
        
        # Scroll and highlight for visibility
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", excel_icon)
        driver.execute_script("arguments[0].style.border='3px solid red';", excel_icon)
        time.sleep(1)
        
        # Get current files in download directory
        initial_files = set(os.listdir(download_dir))
        
        # Try different click methods - improved for <a> tags
        click_methods = [
            ("Regular click", lambda: excel_icon.click()),
            ("JavaScript click", lambda: driver.execute_script("arguments[0].click();", excel_icon)),
            ("ActionChains click", lambda: ActionChains(driver).move_to_element(excel_icon).pause(0.5).click().perform()),
            ("ActionChains with JavaScript", lambda: ActionChains(driver).move_to_element(excel_icon).pause(0.5).perform() and driver.execute_script("arguments[0].click();", excel_icon)),
            ("Parent element click", lambda: excel_icon.find_element(By.XPATH, "..").click() if excel_icon.tag_name == 'img' else excel_icon.click())
        ]
        
        download_successful = False
        for method_name, method in click_methods:
            try:
                print(f"Trying {method_name}...")
                method()
                time.sleep(5)  # Wait longer for download to initiate
                
                # Check for new files
                current_files = set(os.listdir(download_dir))
                new_files = current_files - initial_files
                csv_or_excel = [f for f in new_files if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
                
                if csv_or_excel:
                    print(f"✅ Download successful! New files: {csv_or_excel}")
                    download_successful = True
                    break
                else:
                    print(f"⚠️ No download detected with {method_name}")
            except Exception as e:
                print(f"❌ {method_name} failed: {str(e)}")
        
        if not download_successful:
            print("❌ All click methods attempted but no download detected")
            # Take screenshot for debugging
            driver.save_screenshot("download_button_debug.png")
            print("📸 Saved screenshot as 'download_button_debug.png'")
    else:
        print("❌ Could not locate Excel download button")
        # Take screenshot for debugging
        driver.save_screenshot("download_button_debug.png")
        print("📸 Saved screenshot as 'download_button_debug.png'")

finally:
    driver.quit()
    print("✅ Script completed")