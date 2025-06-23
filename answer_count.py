from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# ✅ Step 0: Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 40)

# ✅ Step 1: Open Internal SME Portal
driver.get("https://sme-automation-portal.com")  # ✅ Professional dummy URL

# 🔐 Enter username & password
wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("sme.user@smeautomation.com")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='action']"))).click()
wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("YourSecurePassword123!")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='action']"))).click()

# ✅ Optional: Check for login error
try:
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'invalid')]"))
    )
    print("❌ Invalid portal credentials!")
    driver.quit()
    exit()
except:
    print("✅ Portal credentials accepted.")

# ✅ Step 2: Open Webmail in New Tab
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get("https://mail.smeautomation.com")  # ✅ Professional dummy email domain

# 🔐 Login to webmail
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='user']"))).send_keys("sme.user@smeautomation.com")
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pass']"))).send_keys("YourMailPassword123!")
wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login_submit']"))).click()

# ✅ Check if login failed
time.sleep(3)
if "login" in driver.current_url.lower():
    print("❌ Invalid Webmail credentials!")
    driver.quit()
    exit()
else:
    print("✅ Webmail login successful.")

# ✅ Step 3: Monitor for OTP Email
time.sleep(5)
initial_count_text = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='rcmcountdisplay']"))).text
initial_count = int(initial_count_text.split()[-1])
print(f"📩 Initial email count: {initial_count}")
print("⏳ Waiting for OTP email...")

max_wait_time = 180
start_time = time.time()
new_email_found = False

while time.time() - start_time < max_wait_time:
    driver.refresh()
    time.sleep(5)
    updated_count_text = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='rcmcountdisplay']"))).text
    updated_count = int(updated_count_text.split()[-1])

    if updated_count > initial_count:
        print(f"✅ New email received! Count: {updated_count}")
        new_email_found = True
        break
    else:
        print("🔄 Waiting...")

if not new_email_found:
    print("❌ OTP not received in time.")
    driver.quit()
    exit()

# ✅ Step 4: Extract OTP from Latest Email
try:
    latest_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[contains(@class, 'message')][1]")))
    latest_email.click()
    time.sleep(5)

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        driver.switch_to.frame(iframes[0])

    email_body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
    otp_match = re.search(r'\b\d{6}\b', email_body)
    otp = otp_match.group(0) if otp_match else None

    if not otp:
        print("❌ OTP extraction failed.")
        driver.quit()
        exit()

    print("✅ Extracted OTP:", otp)
    driver.switch_to.default_content()
except Exception as e:
    print(f"❌ Error extracting OTP: {e}")
    driver.quit()
    exit()

# ✅ Step 5: Enter OTP in Portal
driver.switch_to.window(driver.window_handles[0])
otp_input = wait.until(EC.presence_of_element_located((By.NAME, "code")))
otp_input.send_keys(otp)
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue']"))).click()

# ✅ Validate OTP Entry
try:
    WebDriverWait(driver, 6).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'invalid') or contains(text(),'expired')]"))
    )
    print("❌ Invalid or expired OTP!")
    driver.quit()
    exit()
except:
    print("✅ OTP accepted. Logged in successfully.")

# ✅ Step 6: Navigate to Dashboard → "My Past Work"
print("📂 Navigating to SME dashboard...")

try:
    past_work = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'My Past Work')]")))
    driver.execute_script("arguments[0].scrollIntoView();", past_work)
    time.sleep(2)
    past_work.click()

    question_solving = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-test='dashboard-nav-my-activities-qna-authoring']")))
    driver.execute_script("arguments[0].scrollIntoView();", question_solving)
    time.sleep(2)
    question_solving.click()
except Exception as e:
    print(f"❌ Error navigating to dashboard: {e}")

# ✅ Step 7: Count Submitted Answers by Date
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)

wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-test="answer-date"]')))
days = driver.find_elements(By.XPATH, '//div[@data-test="answer-date"]/div[1]')
months_years = driver.find_elements(By.XPATH, '//div[@data-test="answer-date"]/div[2]')

target_date = "17 May 25"
count = 0

for day, month_year in zip(days, months_years):
    full_date = f"{day.text.strip()} {month_year.text.strip()}"
    print(f"Extracted Date: '{full_date}'")
    if full_date == target_date:
        count += 1

print(f"✅ Total answers submitted on {target_date}: {count}")
driver.quit()