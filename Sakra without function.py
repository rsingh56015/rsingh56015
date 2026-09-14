from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import sys
import io
import os
import re
import textwrap
from fpdf import FPDF
from fpdf.enums import XPos, YPos

sys.stdout.reconfigure(encoding='utf-8')

#driver.implicity_wait(5)
# ── Browser Setup ──
options = Options()
options.add_argument("--force-device-scale-factor=0.88")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()   # we use chrome driver for firefox need webdrive.firefox
driver.maximize_window()
driver.get("https://metacrm.k8s-dev.hlthclub.in/login?tenant=sakra&returnUrl=%2Fsakra%2Fapp%2Fsakra%2Flead%2Flist")  #to call the url
driver.execute_script("document.body.style.zoom='90%'")
print(driver.title)
wait = WebDriverWait(driver, 20)

# Enter the username
username_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='email']")
    ))
username_input.send_keys("admin@dev.com")
print("Username entered: admin@dev.com")

password_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='password']")
    ))
password_input.send_keys("Cu*ost93A#r&")
print("Password entered: Cu*ost93A#r&")

submit_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[normalize-space()='Sign in']")
))
submit_btn.click()
print("Login successful")
time.sleep(2)

all_leads = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/button[3]")
    )
)
all_leads.click()
print("All Leads tab clicked")
time.sleep(2)
'''
all_leads_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='All']]"))
)
print(f"All Leads Count: {all_leads_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#------------------------------------------------------------------------------------
#                               New Lead
#------------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='New']]"))
)
lead.click()
print(f"✅ New Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='New']]"))
)
print(f"✅ New Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#-------------------------------------------------------------------------------------
#                                   Valid Leads
#-------------------------------------------------------------------------------------        

lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='Valid']]"))
)
lead.click()
print(f"✅ Valid Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='Valid']]"))
)
print(f"✅ Valid Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#-------------------------------------------------------------------------------------
#                               Follow Up Lead
#-------------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='Follow Up']]"))
)
lead.click()
print(f"✅ Follow Up Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='Follow Up']]"))
)
print(f"✅ Follow Up Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#-------------------------------------------------------------------------------------
#                               Converted Lead
#-------------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='Converted']]"))
)
lead.click()
print(f"✅ Converted Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='Converted']]"))
)
print(f"✅ Converted Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#-------------------------------------------------------------------------------------
#                               Denied Lead
#-------------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='Denied']]"))
)
lead.click()
print(f"✅ Denied Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='Denied']]"))
)
print(f"✅ Denied Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)

#-------------------------------------------------------------------------------------
#                               Invalid Lead
#-------------------------------------------------------------------------------------
lead = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//text()[normalize-space()='Invalid']]"))
)
lead.click()
print(f"✅ Invalid Lead button clicked")
time.sleep(2)

lead_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='Invalid']]"))
)
print(f"✅ Invalid Lead Count: {lead_count.text}")
time.sleep(2)

#Open 1st lead
first_lead = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_lead.text.strip()
print(f"First Lead Patient Name: {patient_name}")
driver.execute_script("arguments[0].click();", first_lead)
print(f"✅ 1st lead opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)'''

#------------------------------------------------------------------------------------
#                                      Task
#------------------------------------------------------------------------------------
task = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Tasks']"))
)
task.click()
print(f"✅ Task tab clicked")
time.sleep(2)

all_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/button[3]"))
)
all_tasks.click()
print(f"✅ All Task button clicked")
time.sleep(2)

task_count = wait.until(
    EC.presence_of_element_located((By.XPATH,"//button[.//text()[normalize-space()='All']]"))
)
print(f"✅ All Task Count: {task_count.text}")
time.sleep(2)

#Open 1st lead
first_task = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"(//tbody/tr[@data-slot='table-row'])[1]//td[1]//div[contains(@class,'cursor-pointer')]")
    )
)
# Get patient name
patient_name = first_task.text.strip()
print(f"First Task: {patient_name}")
driver.execute_script("arguments[0].click();", first_task)
print(f"✅ 1st task opened successfully")
time.sleep(3)

#Open Associated Leads
associated_leads = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Leads'])[1]"))
)
associated_leads.click()
print(f"✅ Associated Leads tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Associated lead : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated lead : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Lead : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Lead : Patient name: {patient_name}")
time.sleep(2)

assoicated_tasks = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Associated Tasks'])[1]"))
)
assoicated_tasks.click()
print(f"✅ Associated Tasks tab clicked")
time.sleep(3)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Assoicated Task : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Associated Task : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
contact1.click()
print(f"Associated Task : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Associated Task : Patient name: {patient_name}")
time.sleep(2)

transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[4]"))
)
transactions.click()
print(f"✅ Transactions tab clicked :")
time.sleep(3)

# Wait for transaction section
transaction_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find transaction cards
total_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(total_transaction)}")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Transactions : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Transactions : Total contacts: {total_contacts}")

#User Select the 1st patient from the patient list
contact1 = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/span[1]"))
)
contact1.click()
print(f"Transactions : First Patient is selected")

#User is able to see the patient name in the contact dropdown
patient_name = contact.text.strip()
print(f"Transactions : Patient name:{patient_name}")
time.sleep(2)

Patient_transaction = transaction_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Transactions: {len(Patient_transaction)}")

Activity_history = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Activity History']"))
)
Activity_history.click()
print("✅ Activity History tab clicked")
time.sleep(2)

select_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='min-w-0 truncate flex-1 text-left'])[1]"))
)
select_type.click()
print("✅ Select Type Dropdown open successfully")

# User is able to see the type list in type dropdown
type = driver.find_elements(
    By.XPATH,"//div[@data-radix-popper-content-wrapper]//div[@tabindex='-1']"
)
total_type = len(type)
print(f"✅ Select Type Dropdown : Total Type: {total_type}")
time.sleep(2)

lead_type = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//span[@class='block whitespace-nowrap overflow-hidden text-ellipsis'][normalize-space()='Lead']"))
)
lead_type.click()
print(f"✅ Lead Type is selected")
time.sleep(2)

#Select contact from the contact dropdown
contact = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//span[@class='truncate capitalize'])[1]"))
)
contact.click()
print("Activity History : Contact Dropdown open successfully")

# User is able to see the patient list in contact dropdown
patient_list = driver.find_elements(
    By.XPATH,
    "//div[@data-slot='command-list']//div[@data-slot='command-item']"
)
total_contacts = len(patient_list)
print(f"📋Activity History : Total contacts: {total_contacts}")
time.sleep(2)

select_patient = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"))
)
select_patient.click()
print(f"✅ Patient is selected")
time.sleep(2)

#Find the total Task in Activity History
activity_history_section = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'relative') and contains(@class,'m-4')]")
    )
)

# Find activity history cards
total_activity = activity_history_section.find_elements(
    By.XPATH,
    ".//div[contains(@class,'mb-5') and contains(@class,'items-stretch')]"
)
print(f"✅ Total Activity: {len(total_activity)}")
time.sleep(2)

details = wait.until(
    EC.element_to_be_clickable((By.XPATH,"(//button[normalize-space()='Details'])[1]"))
)
details.click()
print(f"✅ Details tab clicked")
time.sleep(2)

back_to_list = wait.until(
    EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[1]"))
)
back_to_list.click()
print(f"✅ Back to list clicked")
time.sleep(2)


time.sleep(5)
driver.quit()
