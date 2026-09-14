from selenium import webdriver #to import selenim webdriver
from selenium.webdriver.chrome.service import Service # to import chrome services
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # to user wait function
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta  #use for select the date as per week or month define in code
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

#driver.implicity_wait(5)
# ── Browser Setup ──
options = Options()
options.add_argument("--force-device-scale-factor=0.75")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()   # we use chrome driver for firefox need webdrive.firefox
driver.maximize_window()
driver.get("https://uatmedi-crmui.medanta.org:5443/medanta/crm/login")  #to call the url
driver.execute_script("document.body.style.zoom='75%'")
print(driver.title)
wait = WebDriverWait(driver, 30)
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
'''
#close through
calendar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='moreFilters_range']"))
)
calendar.click()
print("User clicked on the Calendar")
time.sleep(2)

#User remove the date filter
remove_date = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-picker-clear']"))
)
remove_date.click()
print("Date should be remove by click on clear button")
time.sleep(10)

rows = driver.find_elements(
    By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Rows found: {len(rows)}")

#Open 1st ticket
first_ticket = rows[0].find_element(By.XPATH, ".//a[contains(@class,'bold-600')]")
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", first_ticket
)
time.sleep(3)
driver.execute_script("arguments[0].click();", first_ticket)
print("✅ 1st ticket opened successfully")
time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(10)

try:
# 2️⃣Select the 1st patient from the dropdown list
    patient = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]"))
    )
    time.sleep(5)
    patient.click()
    print("1st patient is selected")

# User click on 3 dot
    dot = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
    )
    time.sleep(2)
    dot.click()
    print("User click on 3dot to view the history of the appointment")

#User click on History button to view the history
    history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
    )
    history.click()
    print("History of this transaction has been open")
    time.sleep(3)

#User want to see the payment history
    payment_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
    )
    payment_history.click()
    print("Hisotry of this transaction has been open and Patient Journey is visibile")
    time.sleep(7)

#User click on cross to close the history
    close_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
    )
    close_history.click()
    print("History section is now close and come back to the transaction page")
    time.sleep(3)

except Exception as e:
    print(f"⚠️ No message available or error occurred: {e}")
    print("⏭️ Skipping message interaction and moving to next section...")
    time.sleep(2)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Ticket Details page
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("Back to the ticket detail tab after clicking")
time.sleep(5)

# Go back to the Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_ticket_page.click()
print("Back to the ticket page by clicking on the back button")
time.sleep(5)

# User click on More Filter button to apply the filter
more_filter = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='More Filters']"))
)
more_filter.click()
print("User click on the More Filter button to apply the filter")
time.sleep(2)

# Select any one agent in the agent filter
agent = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='moreFilters']/div/div[1]/div/div/div[2]/div"))
)
agent.click()
print("User click on the agent field to apply the agent filter")
time.sleep(3)

print("👉 Any one agent is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one branch in the branch filter
branch = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))
)
branch.click()
print("User click on the branch field to apply the branch filter")
time.sleep(3)

print("👉 Any one branch is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one ticket type in the ticket type filter
ticket_type = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))
)
ticket_type.click()
print("User click on the ticket_type field to apply the ticket_type filter")

print("👉 Any one ticket_type is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one ticket sub type in the ticket sub type filter
ticket_sub_type = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))
)
ticket_sub_type.click()
print("User click on the ticket_sub_type field to apply the ticket_sub_type filter")

print("👉 Any one ticket_sub_type is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one category in the category filter
category = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))
)
category.click()
print("User click on the category field to apply the category filter")

print("👉 Any one category is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one priority in the priority filter
priority = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[6]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))
)
priority.click()
print("User click on the priority field to apply the priority filter")

print("👉 Any one priority is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

#Select any one source in the source filter
source = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='moreFilters_source_id']"))
)
source.click()
print("User click on the source field to apply the source filter")

print("👉 Any one source is selectable by the user or if not selected then it is passed blank")
time.sleep(5)

# User click on More Filter button to apply the filter
more_filter = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='More Filters']"))
)
#more_filter.click()
driver.execute_script("arguments[0].click();", more_filter)
print("User click on the More Filter button to apply the filter")
time.sleep(5)

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
start_day = (datetime.today() - timedelta(days=3)).day ##Select a date 7 days before today's date
end_day = datetime.today().day
print(f"Selecting dates: Start={start_day}, End={end_day}")  # f is use for string

# Open calendar
date_range_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body/div/div[@class='ant-modal-root']/div[@class='ant-modal-wrap ant-modal-centered']/div[@role='dialog']/div[@class='ant-modal-content']/div[@class='ant-modal-body']/form[@class='ant-form ant-form-horizontal crm-form']/div[2]/div[1]/div[2]"))
)
date_range_input.click()
time.sleep(10)

# Wait for popup
wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'ant-picker-dropdown')]"))
)

# Click START date (befor 7 days from the today)
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
time.sleep(5)
end_date.click()
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
email_field.send_keys("rsingh@gmail.com")
print("Email rsingh56019@gmail.com is passed in the email field")
time.sleep(5)

#Click on the Submit button
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Submit']"))
)
submit.click()
print("The submit button is clicked to send the email and ticket report file is send to the email")
time.sleep(10)

#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Close)
#------------------------------------------------------------------------------------------------
#move to the next close tab
close = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Closed']"))
)
close.click()
print("Now page are move to the close tab")
time.sleep(5)

# ───────────────────────── WAIT FOR CLOSED TICKET TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH CLOSED TICKET ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Closed tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No closed tickets available")
else:
    # ───────────────────────── OPEN 1ST CLOSED TICKET ─────────────────────────
    first_closed_ticket = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_closed_ticket
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_closed_ticket
    )
    print("✅ 1st Closed ticket opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(10)

try:
# 2️⃣Select the 1st patient from the dropdown list
    patient = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
    )
    time.sleep(2)
    patient.click()
    print("1st patient is selected")

# User click on 3 dot
    dot = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
    )
    time.sleep(2)
    dot.click()
    print("User click on 3dot to view the history of the appointment")

#User click on History button to view the history
    history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
    )
    history.click()
    print("History of this transaction has been open")
    time.sleep(3)

#User want to see the payment history
    payment_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
    )
    payment_history.click()
    print("Hisotry of this transaction has been open and Patient Journey is visibile")
    time.sleep(7)

#User click on cross to close the history

    close_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
    close_history.click()
    print("History section is now close and come back to the transaction page")
    time.sleep(3)

except Exception as e:
    print(f"⚠️ No message available or error occurred: {e}")
    print("⏭️ Skipping message interaction and moving to next section...")
    time.sleep(2)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Ticket Details page
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("Back to the ticket detail tab after clicking")
time.sleep(5)

# Go back to the Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_ticket_page.click()
print("Navigate back to the Closed status ticket page by clicking the back button.")
time.sleep(5)
#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Follow-up)
#------------------------------------------------------------------------------------------------
#move to the next close tab
Follow_up = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Follow-up']"))
)
Follow_up.click()
print("Now page are move to the Follow-up tab")
time.sleep(5)

# ───────────────────────── WAIT FOR Follow-up TICKET TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Follow-Up TICKET ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Follow-up tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Follow-up tickets available")
else:
    # ───────────────────────── OPEN 1ST Follow-up TICKET ─────────────────────────
    first_follow_up_ticket = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_follow_up_ticket
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_follow_up_ticket
    )
    print("✅ 1st Follow_up ticket opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

try:
# 2️⃣Select the 1st patient from the dropdown list
    patient = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
    )
    time.sleep(2)
    patient.click()
    print("1st patient is selected")

# User click on 3 dot
    dot = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
    )
    time.sleep(2)
    dot.click()
    print("User click on 3dot to view the history of the appointment")

#User click on History button to view the history
    history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
    )
    history.click()
    print("History of this transaction has been open")
    time.sleep(3)

#User want to see the payment history
    payment_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
    )
    payment_history.click()
    print("Hisotry of this transaction has been open and Patient Journey is visibile")
    time.sleep(7)

#User click on cross to close the history

    close_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
    close_history.click()
    print("History section is now close and come back to the transaction page")
    time.sleep(3)

except Exception as e:
    print(f"⚠️ No message available or error occurred: {e}")
    print("⏭️ Skipping message interaction and moving to next section...")
    time.sleep(2)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Ticket Details page
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("Back to the ticket detail tab after clicking")
time.sleep(5)

# Go back to the Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_ticket_page.click()
print("Navigate back to the Follow-up status ticket page by clicking the back button.")
time.sleep(5)
#close by
#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(On-Hold)
#------------------------------------------------------------------------------------------------
#move to the next close tab

On_Hold = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='On-hold']"))
)
On_Hold.click()
print("Now page are move to the On_Hold tab")

# ───────────────────────── WAIT FOR On-Hold TICKET TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH On-Hold TICKET ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"On-Hold tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No On-Hold tickets available")
else:
    # Wait a little bit extra for the table data to finish refreshing after tab switch
    time.sleep(3)
    
    # Re-fetch rows just in case the DOM updated
    rows = driver.find_elements(
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]/tr[not(contains(@class, 'ant-table-measure-row')) and not(@aria-hidden='true') and not(contains(@class, 'ant-table-placeholder'))]"
    )

    if len(rows) == 0:
        print("⚠️ No valid On-Hold tickets available after waiting")
    else:
        # Locate the ticket link by checking for the link tag specifically instead of just bold class
        first_onhold_ticket = rows[0].find_element(
            By.XPATH, ".//a[contains(@href, '/ticketDetail/') or contains(@class,'bold-600')]"
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            first_onhold_ticket
        )
        time.sleep(2)

        driver.execute_script(
            "arguments[0].click();",
            first_onhold_ticket
        )
        print("✅ 1st On-Hold ticket opened successfully")
        time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

# 2️⃣Select the 1st patient from the dropdown list
try:
# 2️⃣Select the 1st patient from the dropdown list
    patient = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
    )
    time.sleep(2)
    patient.click()
    print("1st patient is selected")

# User click on 3 dot
    dot = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
    )
    time.sleep(2)
    dot.click()
    print("User click on 3dot to view the history of the appointment")

#User click on History button to view the history
    history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
    )
    history.click()
    print("History of this transaction has been open")
    time.sleep(3)

#User want to see the payment history
    payment_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
    )
    payment_history.click()
    print("Hisotry of this transaction has been open and Patient Journey is visibile")
    time.sleep(7)

#User click on cross to close the history

    close_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
    close_history.click()
    print("History section is now close and come back to the transaction page")
    time.sleep(3)

except Exception as e:
    print(f"⚠️ No message available or error occurred: {e}")
    print("⏭️ Skipping message interaction and moving to next section...")
    time.sleep(2)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Ticket Details page
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("Back to the ticket detail tab after clicking")
time.sleep(5)

# Go back to the Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_ticket_page.click()
print("Navigate back to the Follow-up status ticket page by clicking the back button.")
time.sleep(5)

#----------------------------------------------------------------------------------
#             Switch to Next Tab(Expired)
#----------------------------------------------------------------------------------
#move to the next close tab
Expired = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Expired']"))
)
Expired.click()
print("Now page are move to the Expired tab")
time.sleep(5)

# ───────────────────────── WAIT FOR Expired TICKET TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Expired TICKET ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Expired tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Expired tickets available")
else:
    # ───────────────────────── OPEN 1ST Expired TICKET ─────────────────────────
    first_expired_ticket = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_expired_ticket
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_expired_ticket
    )
    print("✅ 1st Expired ticket opened successfully")
    time.sleep(5)

# Go to the Transactions tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("✅ Navigated to Transactions tab")
time.sleep(3)

# Click on patient dropdown
dropdown_input = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']")
    )
)
dropdown_input.click()
print("✅ Patient dropdown clicked")
time.sleep(3)

# Select first patient
patient = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]")
    )
)
patient.click()
print("✅ First patient selected")
time.sleep(3)

# Click on 3-dot menu
dot = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']")
    )
)
dot.click()
print("✅ Clicked on 3-dot menu to view the history of the appointment")
time.sleep(3)

# Click History
history = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']")
    )
)
history.click()
print("✅ History of this transaction has been open")
time.sleep(3)

# Click Payment History tab
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("✅ History of this transaction has been open and Patient Journey is visible")
time.sleep(7)

# Close History modal
close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='close']"))
)
close_history.click()
print("✅ History section is now closed and returned to the transaction page")
time.sleep(3)

# Go to Communication History
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("✅ Communication History opened")
time.sleep(3)

# View first message
view_message = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]")
    )
)
view_message.click()
print("✅ View Message opened to view the last SMS")
time.sleep(5)

# Close message modal
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='close']"))
)
close_message.click()
print("✅ Message closed and returned to the communication page")
time.sleep(5)

# Go to Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("✅ Activity History opened")
time.sleep(5)

# Back to Ticket Details
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("✅ Back to Ticket Details")
time.sleep(5)

# Back to Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']")
    )
)
back_to_ticket_page.click()
print("✅ Navigated back to ticket list")
time.sleep(5)


#----------------------------------------------------------------------------------
#             Switch to Next Tab(Invalid)
#----------------------------------------------------------------------------------
#move to the next close tab
Invalid = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Invalid']"))
)
Invalid.click()
print("Now page are move to the Invalid tab")
time.sleep(5)

# ───────────────────────── WAIT FOR Invalid TICKET TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Invalid TICKET ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Invalid tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Invalid tickets available")
else:
    # ───────────────────────── OPEN 1ST Invalid TICKET ─────────────────────────
    first_invalid_ticket = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_invalid_ticket
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_invalid_ticket
    )
    print("✅ 1st Invalid ticket opened successfully")
    time.sleep(5)

# Go to the Transactions tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("✅ Navigated to Transactions tab")
time.sleep(3)

# Click on patient dropdown
dropdown_input = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']")
    )
)
dropdown_input.click()
print("✅ Patient dropdown clicked")
time.sleep(3)

# Select first patient
patient = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]")
    )
)
patient.click()
print("✅ First patient selected")
time.sleep(3)

# Click on 3-dot menu
dot = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']")
    )
)
dot.click()
print("✅ Clicked on 3-dot menu to view the history of the appointment")
time.sleep(3)

# Click History
history = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']")
    )
)
history.click()
print("✅ History of this transaction has been open")
time.sleep(3)

# Click Payment History tab
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("✅ History of this transaction has been open and Patient Journey is visible")
time.sleep(7)

# Close History modal
close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='close']"))
)
close_history.click()
print("✅ History section is now closed and returned to the transaction page")
time.sleep(3)

# Go to Communication History
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("✅ Communication History opened")
time.sleep(3)

# View first message
view_message = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]")
    )
)
view_message.click()
print("✅ View Message opened to view the last SMS")
time.sleep(5)

# Close message modal
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='close']"))
)
close_message.click()
print("✅ Message closed and returned to the communication page")
time.sleep(5)

# Go to Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("✅ Activity History opened")
time.sleep(5)

# Back to Ticket Details
ticket_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Ticket Details')]"))
)
ticket_detail.click()
print("✅ Back to Ticket Details")
time.sleep(5)

# Back to Ticket page
back_to_ticket_page = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']")
    )
)
back_to_ticket_page.click()
print("✅ Navigated back to ticket list")
time.sleep(5)'''
#---------------------------------------------------------------------------------
#          Now go to the lead tab
#---------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[@title='Leads']//*[name()='svg']"))
)
lead.click()
print("Successfully redirected to the Lead tab")
time.sleep(5)

#clean the calendar data
calendar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='moreFilters_range']"))
)
calendar.click()
print("User clicked on the Calendar")
time.sleep(5)

#User remove the date filter
try:
    remove_date = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-picker-clear']"))
    )
    remove_date.click()
    print("Date should be remove by click on clear button")
except Exception:
    print("⏭️ No date filter to clear or clear button not found, skipping...")
time.sleep(5)

rows = driver.find_elements(
    By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)
print(f"Rows found: {len(rows)}")
'''
#open 1st lead
first_lead = rows[0].find_element(By.XPATH, ".//a[contains(@class,'bold-600')]")
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", first_lead
)
time.sleep(3)
driver.execute_script("arguments[0].click();", first_lead)
print("✅ 1st lead opened successfully")
time.sleep(5)

transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(10)

try:
# 2️⃣Select the 1st patient from the dropdown list
    patient = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
    )
    time.sleep(2)
    patient.click()
    print("1st patient is selected")

# User click on 3 dot
    dot = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
    )
    time.sleep(2)
    dot.click()
    print("User click on 3dot to view the history of the appointment")

#User click on History button to view the history
    history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
    )
    history.click()
    print("History of this transaction has been open")
    time.sleep(3)

#User want to see the payment history
    payment_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
    )
    payment_history.click()
    print("Hisotry of this transaction has been open and Patient Journey is visibile")
    time.sleep(7)

#User click on cross to close the history

    close_history = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
    )
    close_history.click()
    print("History section is now close and come back to the transaction page")
    time.sleep(3)

except Exception as e:
    print(f"⚠️ No message available or error occurred: {e}")
    print("⏭️ Skipping message interaction and moving to next section...")
    time.sleep(2)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
driver.execute_script("arguments[0].click();", communication_history)
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Ticket Details page
lead_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Lead Details')]"))
)
lead_detail.click()
print("Back to the ticket detail tab after clicking")
time.sleep(5)

# Go back to the Ticket page
back_to_lead_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_lead_page.click()
print("Back to the lead page by clicking on the back button")
time.sleep(5)

#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Follow-up)
#------------------------------------------------------------------------------------------------
#move to the next Followup tab
Follow_up = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Follow-up']"))
)
Follow_up.click()
print("Now page are move to the Follow-up tab")
time.sleep(5)

#Open 1st LEAD
# ───────────────────────── WAIT FOR Follow-up LEAD TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Follow-Up LEAD ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Follow-up tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Follow-up LEADs available")
else:
    # ───────────────────────── OPEN 1ST Follow-up LEAD ─────────────────────────
    first_follow_up_lead = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_follow_up_lead
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_follow_up_lead
    )
    print("✅ 1st Follow_up lead opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

# 2️⃣Select the 1st patient from the dropdown list
patient = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
)
patient.click()
print("1st patient is selected")
time.sleep(3)

# User click on 3 dot
dot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
)
dot.click()
print("User click on 3dot to view the history of the appointment")
time.sleep(3)

#User click on History button to view the history 
history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
)
history.click()
print("History of this transaction has been open")
time.sleep(3)

#User want to see the payment history
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("Hisotry of this transaction has been open and Patient Journey is visibile")
time.sleep(7)

#User click on cross to close the history

close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_history.click()
print("History section is now close and come back to the transaction page")
time.sleep(3)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Lead Details page
lead_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Lead Details')]"))
)
lead_detail.click()
print("Back to the lead detail tab after clicking")
time.sleep(5)

# Go back to the Lead page
back_to_lead_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_lead_page.click()
print("Navigate back to the Follow-up status lead page by clicking the back button.")
time.sleep(5)

#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Converted)
#------------------------------------------------------------------------------------------------
#move to the next Converted tab
Converted = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Converted']"))
)
Converted.click()
print("Now page are move to the Converted-up tab")
time.sleep(5)

#Open 1st LEAD
# ───────────────────────── WAIT FOR Converted LEAD TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Converted LEAD ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Converted tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Converted LEADs available")
else:
    # ───────────────────────── OPEN 1ST Converted LEAD ─────────────────────────
    first_converted_lead = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_converted_lead
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_converted_lead
    )
    print("✅ 1st Converted lead opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicking")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

# 2️⃣Select the 1st patient from the dropdown list
patient = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
)
patient.click()
print("1st patient is selected")
time.sleep(3)

# User click on 3 dot
dot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
)
dot.click()
print("User click on 3dot to view the history of the appointment")
time.sleep(3)

#User click on History button to view the history 
history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
)
history.click()
print("History of this transaction has been open")
time.sleep(3)

#User want to see the payment history
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("Hisotry of this transaction has been open and Patient Journey is visibile")
time.sleep(7)

#User click on cross to close the history

close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_history.click()
print("History section is now close and come back to the transaction page")
time.sleep(3)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Lead Details page
lead_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Lead Details')]"))
)
lead_detail.click()
print("Back to the lead detail tab after clicking")
time.sleep(5)

# Go back to the Lead page
back_to_lead_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_lead_page.click()
print("Navigate back to the Converted status lead page by clicking the back button.")
time.sleep(5)

#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Denied)
#------------------------------------------------------------------------------------------------
#move to the next Denied tab
Denied = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Denied']"))
)
Denied.click()
print("Now page are move to the Denied-up tab")
time.sleep(5)

#Open 1st LEAD
# ───────────────────────── WAIT FOR Denied LEAD TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Denied LEAD ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Denied tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Denied LEADs available")
else:
    # ───────────────────────── OPEN 1ST Denied LEAD ─────────────────────────
    first_Denied_lead = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_Denied_lead
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_Denied_lead
    )
    print("✅ 1st Denied lead opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicking")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

# 2️⃣Select the 1st patient from the dropdown list
patient = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
)
patient.click()
print("1st patient is selected")
time.sleep(3)

# User click on 3 dot
dot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
)
dot.click()
print("User click on 3dot to view the history of the appointment")
time.sleep(3)

#User click on History button to view the history 
history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
)
history.click()
print("History of this transaction has been open")
time.sleep(3)

#User want to see the payment history
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("Hisotry of this transaction has been open and Patient Journey is visibile")
time.sleep(7)

#User click on cross to close the history

close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_history.click()
print("History section is now close and come back to the transaction page")
time.sleep(3)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Lead Details page
lead_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Lead Details')]"))
)
lead_detail.click()
print("Back to the lead detail tab after clicking")
time.sleep(5)

# Go back to the Lead page
back_to_lead_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_lead_page.click()
print("Navigate back to the Denied status lead page by clicking the back button.")
time.sleep(5)


#------------------------------------------------------------------------------------------------
#                                 Switch to Next Tab(Closed)
#------------------------------------------------------------------------------------------------
#move to the next Closed tab
Closed = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Closed']"))
)
Closed.click()
print("Now page are move to the Closed-up tab")
time.sleep(5)

#Open 1st LEAD
# ───────────────────────── WAIT FOR Closed LEAD TABLE ─────────────────────────
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    )
)

# ───────────────────────── FETCH Closed LEAD ROWS ─────────────────────────
rows = driver.find_elements(
    By.XPATH,
    "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Closed tab rows found: {len(rows)}")

if len(rows) == 0:
    print("⚠️ No Closed LEADs available")
else:
    # ───────────────────────── OPEN 1ST Closed LEAD ─────────────────────────
    first_Closed_lead = rows[0].find_element(
        By.XPATH, ".//a[contains(@class,'bold-600')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        first_Closed_lead
    )
    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        first_Closed_lead
    )
    print("✅ 1st Closed lead opened successfully")
    time.sleep(5)

#Go to the transaction tab
transaction = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Transactions')]"))
)
transaction.click()
print("Go to the transaction tab after clicking")
time.sleep(3)

# 1️⃣ Click on the dropdown input
dropdown_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/input[1]"))
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']"))
)
dropdown_input.click()
print("dropdown is clickable")
time.sleep(3)

# 2️⃣Select the 1st patient from the dropdown list
patient = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]"))
)
patient.click()
print("1st patient is selected")
time.sleep(3)

# User click on 3 dot
dot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']"))
)
dot.click()
print("User click on 3dot to view the history of the appointment")
time.sleep(3)

#User click on History button to view the history 
history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']"))
)
history.click()
print("History of this transaction has been open")
time.sleep(3)

#User want to see the payment history
payment_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
)
payment_history.click()
print("Hisotry of this transaction has been open and Patient Journey is visibile")
time.sleep(7)

#User click on cross to close the history

close_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_history.click()
print("History section is now close and come back to the transaction page")
time.sleep(3)

#Go to the Communication History tab
communication_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Communication History')]"))
)
communication_history.click()
print("Go to the transaction tab after clicing")
time.sleep(3)

# User check the fist message to check view message button is working fine or not
view_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]"))
)
view_message.click()
print("View message button is working fine and user able to view the last sms")
time.sleep(5)

#close the open message
close_message = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
)
close_message.click()
print("Message is now close and come back to the communication page")
time.sleep(5)

#Go to the Activity History
activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Activity History')]"))
)
activity_history.click()
print("Go to the activity history tab after clicking")
time.sleep(5)

# Go back to the Lead Details page
lead_detail = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Lead Details')]"))
)
lead_detail.click()
print("Back to the lead detail tab after clicking")
time.sleep(5)

# Go back to the Lead page
back_to_lead_page = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
)
back_to_lead_page.click()
print("Navigate back to the Closed status lead page by clicking the back button.")
time.sleep(5)

# Back to Lead page
back_to_newlead_tab = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='New']")
    )
)
back_to_newlead_tab.click()
print("✅ Navigated back to New lead list")
time.sleep(5)

rows = driver.find_elements(
    By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
)

print(f"Rows found: {len(rows)}")
'''
#open 1st lead
first_lead = rows[0].find_element(By.XPATH, ".//a[contains(@class,'bold-600')]")
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", first_lead
)
time.sleep(3)
driver.execute_script("arguments[0].click();", first_lead)
print("✅ 1st lead opened successfully")
time.sleep(5)

#Click on the consult option to book consult appointment
consult = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Doctor Consult')]"))
)
consult.click()
print("Consult Service is now clicked to book consult appointment")
time.sleep(5)

#Go to the All Booking Section 
all_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, " //span[normalize-space()='All Bookings']"))
)
all_booking.click()
print("Go to the All booking tab to check the all booked consult appoitnment")
time.sleep(5)

#back to the New booking page
new_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
)
new_booking.click()
print("Go back to the New Booking tab to book an appointment")
time.sleep(5)

# 1️⃣ Click on the Select Region dropdown input
region_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
)
region_dropdown_input.click()
print("Select Region dropdown is clickable")
time.sleep(3)

first_region_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]"))
)
first_region_select.click()
print("✅ First region selected successfully")
time.sleep(3)

# 1️⃣ Click on the Select hospital dropdown input
hospital_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
)
hospital_dropdown_input.click()
print("Select hospital dropdown is clickable")
time.sleep(5)

first_hospital_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]"))
)
first_hospital_select.click()
print("✅ First hospital selected successfully")
time.sleep(3)

search = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
search.click()
print("Search button is clicked")
time.sleep(3)

earliest_availability = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]"))
)
earliest_availability.click()
print("✅ Earliest availability button is clicked successfully")
time.sleep(5)

select_slot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]"))
)
select_slot.click()
print("✅ Select slot button is clicked successfully")
time.sleep(7)

def select_first_available_slot():
    try:
        print("Looking for available time slots...")
        
        # 1. Wait for the slot container to be visible
        # We target the 'ant-col' that contains the slot-time class
        slot_xpath = "(//div[contains(@class, 'slot-time')])[1]"
        
        # 2. Wait until the first slot is clickable
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        
        # 3. Use JavaScript click to ensure the selection is registered 
        # (This avoids issues with the 'active' blue border overlay)
        driver.execute_script("arguments[0].click();", first_slot)
        
        # Verify if a specific time was selected (Optional logging)
        selected_time = first_slot.text
        print(f"✅ Successfully selected the 1st slot: {selected_time}")

    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select the time slot: {e}")

# Run the function
select_first_available_slot()
time.sleep(2)

add_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']"))
)
add_to_cart.click()
print("✅ Add to cart button is clicked successfully")
time.sleep(3)

proceed_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]"))
    #EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']']"))
)
proceed_to_cart.click()
print("✅ Proceed to cart button is clicked successfully")
time.sleep(8)


edit_the_slots = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-row ant-row-end']//div[3]//*[name()='svg']"))
)
edit_the_slots.click()
print("✅ Edit the slots button is clicked successfully")
time.sleep(10)

def select_first_available_slot():
    try:
        print("Looking for available time slots...")
        
        # 1. Wait for the slot container to be visible
        # We target the 'ant-col' that contains the slot-time class
        slot_xpath = "(//div[contains(@class, 'slot-time')])[1]"
        
        # 2. Wait until the first slot is clickable
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        
        # 3. Use JavaScript click to ensure the selection is registered 
        # (This avoids issues with the 'active' blue border overlay)
        driver.execute_script("arguments[0].click();", first_slot)
        
        # Verify if a specific time was selected (Optional logging)
        selected_time = first_slot.text
        print(f"✅ Successfully selected the 1st slot: {selected_time}")

    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select the time slot: {e}")

# Run the function
select_first_available_slot()
time.sleep(2)

add_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
add_to_cart.click()
print("✅ Add to cart button is clicked successfully")
time.sleep(5)

proceed_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]"))
    #EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']']"))
)
proceed_to_cart.click()
print("✅ Proceed to cart button is clicked successfully")
time.sleep(5)
'''
'''
Add_more_services = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-lg ant-btn-block crm-outline-btn']"))
)
Add_more_services.click()
print("✅ Add more services button is clicked successfully")
time.sleep(3)

Radiology_OD = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-modal-body')]//div[2]//button[1]"))
)
Radiology_OD.click()
print("✅ Radiology/Other Diagnostic button is clicked successfully")
time.sleep(3)

Radiology = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-row service-selection')]//div[1]//button[1]"))
)
Radiology.click()
print("✅ Radiology button is clicked successfully")
time.sleep(3)

#Go to the All Booking Section 
all_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, " //span[normalize-space()='All Bookings']"))
)
all_booking.click()
print("Go to the All booking tab to check the all booked consult appoitnment")
time.sleep(5)

#back to the New booking page
new_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
)
new_booking.click()
print("Go back to the New Booking tab to book an appointment")
time.sleep(5)

region_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
)
region_dropdown_input.click()
print("Select Region dropdown is clickable")
time.sleep(3)

first_region_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]"))
)
first_region_select.click()
print("✅ First region selected successfully")
time.sleep(3)

# 1️⃣ Click on the Select hospital dropdown input
hospital_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
)
hospital_dropdown_input.click()
print("Select hospital dropdown is clickable")
time.sleep(3)

first_hospital_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]"))
)
first_hospital_select.click()
print("✅ First hospital selected successfully")
time.sleep(3)

Modality = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-select-selection-search'])[5]"))
)
Modality.click()
print("✅ Modality dropdown is clicked successfully")
time.sleep(3)

# Scrollable dropdown container
dropdown = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]"))
)

# Try to find option
found = False

for i in range(10):   # scroll attempts
    try:
        option = driver.find_element(
            By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='COMPUTERISED TOMOGRAPHY']"
        )
        driver.execute_script("arguments[0].click();", option)
        print("✅ COMPUTERIZED TOMOGRAPHY selected")
        found = True
        break
    except:
        # Scroll down
        driver.execute_script("arguments[0].scrollTop += 200", dropdown)
        time.sleep(2)
if not found:
    print("❌ COMPUTERIZED TOMOGRAPHY not found in dropdown")

Radiologytest = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))
)
Radiologytest.click()
print("✅ Radiology test dropdown is clicked successfully")
time.sleep(3)

# Scrollable dropdown container
dropdown = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]"))
)

# Try to find option
found = False

for i in range(10):   # scroll attempts
    try:
        option = driver.find_element(
            By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='CT ANGIOGRAPHY BRAIN']"
        )
        driver.execute_script("arguments[0].click();", option)
        print("✅ CT ANGIOGRAPHY BRAIN selected")
        found = True
        break
    except:
        # Scroll down
        driver.execute_script("arguments[0].scrollTop += 200", dropdown)
        time.sleep(2)
if not found:
    print("❌ CT ANGIOGRAPHY BRAIN not found in dropdown")

Search = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
Search.click()
print("✅ Search button is clicked successfully")
time.sleep(5)

earliest_availability = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"))
)
earliest_availability.click()
print("✅ Earliest availability button is clicked successfully")
time.sleep(5)

select_slot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]"))
)
select_slot.click()
print("✅ Select slot button is clicked successfully")
time.sleep(7)

def select_first_available_slot():
    try:
        print("Looking for available time slots...")
        
        # 1. Wait for the slot container to be visible
        # We target the 'ant-col' that contains the slot-time class
        slot_xpath = "(//div[contains(@class, 'slot-time')])[1]"
        
        # 2. Wait until the first slot is clickable
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        
        # 3. Use JavaScript click to ensure the selection is registered 
        # (This avoids issues with the 'active' blue border overlay)
        driver.execute_script("arguments[0].click();", first_slot)
        
        # Verify if a specific time was selected (Optional logging)
        selected_time = first_slot.text
        print(f"✅ Successfully selected the 1st slot: {selected_time}")

    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select the time slot: {e}")

# Run the function
select_first_available_slot()
time.sleep(2)

add_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']"))
)
add_to_cart.click()
print("✅ Add to cart button is clicked successfully")
time.sleep(3)

Advising_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-row ant-row-middle']//div[@class='ant-select-selector']"))
)
Advising_doctor.click()
print("✅ Advising doctor dropdown is clicked successfully")
time.sleep(3)

first_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content')]"))
)
first_doctor.click()
print("✅ First doctor is selected successfully")
time.sleep(3)

Add_more_services = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-lg ant-btn-block crm-outline-btn']"))
)
Add_more_services.click()
print("✅ Add more services button is clicked successfully")
time.sleep(3)

Lab_test = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Lab')]"))
)
Lab_test.click()
print("✅ Lab test button is clicked successfully")
time.sleep(3)

Lab_hospital = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Hospital')]"))
)
Lab_hospital.click()
print("✅ Lab @ Hospital option is clicked successfully")
time.sleep(3)

Select_hospital = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-lg')]//div[@class='ant-select-selector']"))
)
Select_hospital.click()
print("✅ Select hospital/Clinic field is clicked successfully")
time.sleep(3)

first_lab_hospital = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content')]"))
)
driver.execute_script("arguments[0].click();", first_lab_hospital)
print("✅ First lab hospital is selected successfully")
time.sleep(3)

continue_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
)
continue_button.click()
print("✅ Continue button is clicked successfully")
time.sleep(3)

#Go to the All Booking Section 
all_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, " //span[normalize-space()='All Bookings']"))
)
all_booking.click()
print("Go to the All booking tab to check the all booked consult appoitnment")
time.sleep(5)

#back to the New booking page
new_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
)
new_booking.click()
print("Go back to the New Booking tab to book an appointment")
time.sleep(5)

Search = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
Search.click()
print("✅ Search button is clicked successfully")
time.sleep(5)

Add_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to Cart')]"))
)
driver.execute_script("arguments[0].click();", Add_to_cart)
print("✅ Add to cart button is clicked successfully")
time.sleep(10)

cart_logo = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='anticon']//*[name()='svg']"))
)
cart_logo.click()
print("✅ Cart logo is clicked successfully and user is redirected to the cart page")
time.sleep(5)

Advising_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-row ant-row-middle']//div[@class='ant-select-selector']"))
)
Advising_doctor.click()
print("✅ Advising doctor dropdown is clicked successfully")
time.sleep(3)

first_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content')]"))
)
first_doctor.click()
print("✅ First doctor is selected successfully")
time.sleep(3)

Add_more_lab = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-text text-primary p-0']"))
)
Add_more_lab.click()
print("✅ Add more lab button is clicked successfully")
time.sleep(5)

add_to_cart_lab = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to Cart')]"))
)
driver.execute_script("arguments[0].click();", add_to_cart_lab)
print("✅ Add to cart button is clicked successfully")
time.sleep(10)

cart_logo = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='anticon']//*[name()='svg']"))
)
cart_logo.click()
print("✅ Cart logo is clicked successfully and user is redirected to the cart page")
time.sleep(5)

select_slot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-text']"))
)
select_slot.click()
print("✅ Select slot button is clicked successfully")
time.sleep(5)

def select_first_available_slot():
    try:
        print("Looking for available time slots...")
        
        # 1. Wait for the slot container to be visible
        # We target the 'ant-col' that contains the slot-time class
        slot_xpath = "(//div[contains(@class, 'slot-time')])[1]"
        
        # 2. Wait until the first slot is clickable
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        
        # 3. Use JavaScript click to ensure the selection is registered 
        # (This avoids issues with the 'active' blue border overlay)
        driver.execute_script("arguments[0].click();", first_slot)
        
        # Verify if a specific time was selected (Optional logging)
        selected_time = first_slot.text
        print(f"✅ Successfully selected the 1st slot: {selected_time}")

    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select the time slot: {e}")

# Run the function
select_first_available_slot()
time.sleep(2)

continue_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
continue_button.click()
print("✅ Continue button is clicked successfully")
time.sleep(5)

Add_more_services = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-lg ant-btn-block crm-outline-btn']"))
)
Add_more_services.click()
print("✅ Add more services button is clicked successfully")
time.sleep(3)

EHC_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'EHC')]"))
)
EHC_button.click()
print("✅ EHC button is clicked successfully")
time.sleep(3)

#Go to the All Booking Section 
all_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, " //span[normalize-space()='All Bookings']"))
)
all_booking.click()
print("Go to the All booking tab to check the all booked consult appoitnment")
time.sleep(5)

#back to the New booking page
new_booking = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
)
new_booking.click()
print("Go back to the New Booking tab to book an appointment")
time.sleep(5)

region_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
)
region_dropdown_input.click()
print("Select Region dropdown is clickable")
time.sleep(3)

first_region_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]"))
)
first_region_select.click()
print("✅ First region selected successfully")
time.sleep(3)

# 1️⃣ Click on the Select hospital dropdown input
hospital_dropdown_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
)
hospital_dropdown_input.click()
print("Select hospital dropdown is clickable")
time.sleep(3)

first_hospital_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]"))
)
first_hospital_select.click()
print("✅ First hospital selected successfully")
time.sleep(3)

EHC_package = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))
)
EHC_package.click()
print("✅ EHC package dropdown is clicked successfully")
time.sleep(3)

# Scrollable dropdown container
dropdown = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]"))
)

# Try to find option
found = False

for i in range(10):   # scroll attempts
    try:
        option = driver.find_element(
            By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='MEDANTA BASIC HEALTH CHECK']"
        )
        driver.execute_script("arguments[0].click();", option)
        print("✅ MEDANTA BASIC HEALTH CHECK selected")
        found = True
        break
    except:
        # Scroll down
        driver.execute_script("arguments[0].scrollTop += 2000", dropdown)
        time.sleep(2)
if not found:
    print("❌ MEDANTA BASIC HEALTH CHECK not found in dropdown")

Search = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']"))
)
Search.click()
print("✅ Search button is clicked successfully")
time.sleep(5)

earliest_availability = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"))
)
earliest_availability.click()
print("✅ Earliest availability button is clicked successfully")
time.sleep(5)

select_slot = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]"))
)
select_slot.click()
print("✅ Select slot button is clicked successfully")
time.sleep(7)

def select_first_available_slot():
    try:
        print("Looking for available time slots...")
        
        # 1. Wait for the slot container to be visible
        # We target the 'ant-col' that contains the slot-time class
        slot_xpath = "(//div[contains(@class, 'slot-time')])[1]"
        
        # 2. Wait until the first slot is clickable
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        
        # 3. Use JavaScript click to ensure the selection is registered 
        # (This avoids issues with the 'active' blue border overlay)
        driver.execute_script("arguments[0].click();", first_slot)
        
        # Verify if a specific time was selected (Optional logging)
        selected_time = first_slot.text
        print(f"✅ Successfully selected the 1st slot: {selected_time}")

    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select the time slot: {e}")

# Run the function
select_first_available_slot()
time.sleep(2)

add_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']"))
)
add_to_cart.click()
print("✅ Add to cart button is clicked successfully")
time.sleep(3)

Advising_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-row ant-row-middle']//div[@class='ant-select-selector']"))
)
Advising_doctor.click()
print("✅ Advising doctor dropdown is clicked successfully")
time.sleep(3)

first_doctor = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content')]"))
)
first_doctor.click()
print("✅ First doctor is selected successfully")
time.sleep(3)

time.sleep(30)
driver.quit()