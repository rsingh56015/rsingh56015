from selenium import webdriver #to import selenim webdriver
from selenium.webdriver.chrome.service import Service # to import chrome services
from selenium.webdriver.support.ui import WebDriverWait  # to user wait function
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta  #use for select the date as per week or month define in code
import time

#driver.implicity_wait(5)
driver = webdriver.Chrome()   # we use chrome driver for firefox need webdrive.firefox
driver.maximize_window()
driver.get("https://uatmedi-crmui.medanta.org:5443/medanta/crm/login")  #to call the url
print(driver.title)
wait = WebDriverWait(driver, 20)
# Enter the 10 digit mobile number

mobile_input = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='number-login_username']")
        #(By.XPATH, "//input[@placeholder='Enter 10 Digit mobile number']") 
    )
)
mobile_input.send_keys("4444444444")
print("mobile number is entered")
# ✅ Click Get OTP
get_otp_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Get OTP']/ancestor::button")
    )
)
get_otp_btn.click()
print("otp page is open")
time.sleep(3)

first_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[1]"])
)
first_otp.send_keys("3")

second_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[2]"])
)
second_otp.send_keys("2")

third_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[3]"])
)
third_otp.send_keys("1")

fourth_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[4]"])
)
fourth_otp.send_keys("5")

fifth_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[5]"])
)
fifth_otp.send_keys("6")

sixth_otp=wait.until(
    EC.visibility_of_element_located(
        [By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[6]"])
)
sixth_otp.send_keys("4")

submit_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[3]/div/button"))
)
submit_button.click()
print("Submit button is automatically clickable-Login Successful")
time.sleep(15)

#----------------------------------------------------------------------------
#Download Ticket Reports 
#----------------------------------------------------------------------------
# User click on download button to download the report
download = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='download']//*[name()='svg']"))
)
download.click()
print("Download button is clicked")
time.sleep(10)

# Ticket Report is selected
ticket_reports = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@value='ticket_report']"))
)
print("Report Type:", ticket_reports.get_attribute("value"))

# Calculate dates
start_day = (datetime.today() - timedelta(days=7)).day ##Select a date 7 days before today's date
end_day = datetime.today().day
print(f"Selecting dates: Start={start_day}, End={end_day}")  # f is use for string

# Open calendar
date_range_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='date_range']"))
)
date_range_input.click()
time.sleep(10)

# Wait for popup
wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'ant-picker-dropdown')]"))
)

# Click START date (befor 7 days from the today)
# Select START date
start_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"(//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{start_day}'])[1]"
    ))
)
driver.execute_script("arguments[0].click();", start_date)
print(f"✅ Start date clicked: {start_day}")
time.sleep(1)

# Select END date
end_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, 
        f"(//div[contains(@class,'ant-picker-panel')])[2]"
        f"//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{end_day}']"
    ))
)
driver.execute_script("arguments[0].click();", end_date)
print(f"✅ End date clicked: {end_day}")
time.sleep(1)

print(f"✅ Date range selected successfully: {start_date}, {end_date}")
time.sleep(1)

# Locate the email input field
email_field = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='email']"))
)
email_field.clear()
print("Email field is selected")

# Select all and delete
email_field.send_keys(Keys.CONTROL + "a")  # Ctrl+A (use Keys.COMMAND + "a" for Mac)
email_field.send_keys(Keys.DELETE)  # or Keys.BACKSPACE
print("Field cleared using Ctrl+A + Delete")
time.sleep(1)

email_field = wait.until(
    EC.visibility_of_element_located([By.XPATH, "//input[@id='email']"])
)
email_field.send_keys("rsingh56019@gmail.com")
print("Email rsingh56019@gmail.com is passed in the email field")
time.sleep(5)

#Click on the Submit button
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Submit']"))
)
submit.click()
print("The submit button is clicked to send the email and ticket report file is send to the email")
time.sleep(10)

#----------------------------------------------------------------------------
#Download Ticket Analysis Reports 
#----------------------------------------------------------------------------

# ✅ User click on download button to download the report
download_analysis = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='download']//*[name()='svg']"))
)
download_analysis.click()
print("Download button is clicked")
time.sleep(10)

# Ticket Analysis Report is selected
ticket_analysis_report = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='type']/div/div[2]/label"))   # type should be in single quote
)
#ticket_analysis_report.click()
driver.execute_script("arguments[0].click();", ticket_analysis_report)
print("✅ Ticket Analysis Report selected")
time.sleep(1)

# Calculate dates
start_day = (datetime.today() - timedelta(days=7)).day ##Select a date 7 days before today's date
end_day = datetime.today().day  

print(f"Selecting dates: Start={start_day}, End={end_day}")

# Open calendar
date_range_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='date_range']"))
)
date_range_input.click()
time.sleep(3)

# Click START date (befor 7 days from the today)
start_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, 
        f"(//div[contains(@class,'ant-picker-panel')])[1]//div[text()='{start_day}']"
    ))
)
time.sleep(0.5)
start_date.click()
print(f"✅ Clicked start date: {start_day}")
time.sleep(2)

# Click END date (today date) 
end_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, 
        f"(//div[contains(@class,'ant-picker-panel')])[2]//div[text()='{end_day}']"
    ))
)
time.sleep(0.5)
end_date.click()
#driver.execute_script("arguments[0].click();", end_date)
print(f"✅ Clicked end date: {end_day}")
time.sleep(2)

print(f"✅ Date range selected successfully: {start_date}, {end_date}")
time.sleep(1)

# Locate the email input field
email_field = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='email']"))
)
email_field.clear()
print("Email field is selected")
time.sleep(1)

# Select all and delete
email_field.send_keys(Keys.CONTROL + "a")  # Ctrl+A (use Keys.COMMAND + "a" for Mac)
email_field.send_keys(Keys.DELETE)  # or Keys.BACKSPACE
print("Field cleared using Ctrl+A + Delete")

email_field = wait.until(
    EC.visibility_of_element_located([By.XPATH, "//input[@id='email']"])
)
email_field.send_keys("rsingh56019@gmail.com")
print("Email rsingh56019@gmail.com is passed in the email field")
time.sleep(5)

#Click on the Submit button
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Submit']"))
)
submit.click()
print("The submit button is clicked to send the ticket analysis report email.")

#----------------------------------------------------------------------------
#Download Ticket Activity Reports 
#----------------------------------------------------------------------------

# User click on download button to download the report
download_activity_report = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='download']//*[name()='svg']"))
)
download_activity_report.click()
time.sleep(10)

# Select Ticket Activity Report (3rd radio button)
ticket_activity_report = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='type']/div/div[3]/label/span[2]")) # type should be in single quote
)
driver.execute_script("arguments[0].click();", ticket_activity_report)
print("✅ Ticket Activity Report selected")
time.sleep(5)

# Calculate dates
start_day = (datetime.today() - timedelta(days=7)).day ##Select a date 7 days before today's date
end_day = datetime.today().day  

print(f"Selecting dates: Start={start_day}, End={end_day}")

# Open calendar
date_range_input = wait.until(                #webdriver.wait
    EC.element_to_be_clickable((By.XPATH, "//input[@id='date_range']"))
)
date_range_input.click()
time.sleep(3)

# Click START date (befor 7 days from the today)
start_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, 
        f"(//div[contains(@class,'ant-picker-panel')])[1]//div[text()='{start_day}']"
    ))
)
start_date.click()
print(f"✅ Clicked start date: {start_day}")
time.sleep(2)

# Click END date (today date) 
end_date = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, 
        f"(//div[contains(@class,'ant-picker-panel')])[2]//div[text()='{end_day}']"
    ))
)
end_date.click()
#driver.execute_script("arguments[0].click();", end_date)
print(f"✅ Clicked end date: {end_day}")
time.sleep(2)

print(f"✅ Date range selected successfully: {start_date}, {end_date}")
time.sleep(1)

# Locate the email input field
email_field = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='email']"))
)
email_field.clear()
print("Email field is selected")

# Select all and delete
email_field.send_keys(Keys.CONTROL + "a")  # Ctrl+A (use Keys.COMMAND + "a" for Mac)
email_field.send_keys(Keys.DELETE)  # or Keys.BACKSPACE
print("Field cleared using Ctrl+A + Delete")
time.sleep(1)

email_field = wait.until(
    EC.visibility_of_element_located([By.XPATH, "//input[@id='email']"])
)
email_field.send_keys("rsingh56019@gmail.com")
print("Email rsingh56019@gmail.com is passed in the email field")
time.sleep(5)

#Click on the Submit button
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Submit']"))
)
submit.click()
print("The submit button is clicked to send the ticket activity report email.")
time.sleep(5)

time.sleep(15)
driver.quit()