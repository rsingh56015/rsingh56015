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

sys.stdout.reconfigure(encoding='utf-8')

# ══════════════════════════════════════════════════════════════
#                     BROWSER SETUP
# ══════════════════════════════════════════════════════════════
def setup_driver():
    options = Options()
    options.add_argument("--force-device-scale-factor=0.75")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='75%'")
    return driver

driver = setup_driver()
wait = WebDriverWait(driver, 30)

# ══════════════════════════════════════════════════════════════
#                     LOGIN FUNCTION
# ══════════════════════════════════════════════════════════════
def login(url, mobile, otp_digits):
    """Login to the CRM portal with mobile number and OTP."""
    try:
        driver.get(url)
        print(driver.title)
        mobile_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='number-login_username']"))
        )
        mobile_input.send_keys(mobile)
        print(f"✅ Mobile number {mobile} entered")

        get_otp_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Get OTP']/ancestor::button"))
        )
        get_otp_btn.click()
        print("✅ OTP page opened")
        time.sleep(3)

        for i, digit in enumerate(otp_digits, start=1):
            otp_input = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[{i}]")
                )
            )
            otp_input.send_keys(digit)

        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[3]/div/button")
            )
        )
        submit_button.click()
        print("✅ Login Successful")
        time.sleep(15)

    except Exception as e:
        print(f"❌ Login failed: {e}")
        raise

# ══════════════════════════════════════════════════════════════
#              COMMON HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
def select_first_available_slot():
    """Selects the first available time slot."""
    try:
        print("🔍 Looking for available time slots...")
        first_slot = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'slot-time')])[3]"))
        )
        driver.execute_script("arguments[0].click();", first_slot)
        print(f"✅ Slot selected: {first_slot.text}")
    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select time slot: {e}")

def clear_calendar_filter():
    """Clears the date filter from calendar."""
    try:
        calendar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='moreFilters_range']"))
        )
        calendar.click()
        print("✅ Calendar clicked")
        time.sleep(2)
        remove_date = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='close-circle']"))
            #EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-picker-clear']"))
        )
        remove_date.click()
        print("✅ Date filter cleared")
    except Exception:
        print("⏭️ No date filter to clear, skipping...")
    time.sleep(5)

def open_first_row(row_type="ticket"):
    """Fetch rows from table and open the first one. Returns False if no rows."""
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]"))
    )
    rows = driver.find_elements(
        By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
    )
    print(f"🔍 Rows found: {len(rows)}")

    if len(rows) == 0:
        print(f"⚠️ No {row_type}s available — skipping this tab")
        return False

    first_item = rows[0].find_element(By.XPATH, ".//a[contains(@class,'bold-600')]")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_item)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", first_item)
    print(f"✅ First {row_type} opened")
    time.sleep(5)
    return True

def go_to_tab(tab_name):
    """Navigate to an inner detail tab."""
    try:
        tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{tab_name}')]"))
        )
        tab.click()
        print(f"✅ Navigated to '{tab_name}' tab")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Could not navigate to '{tab_name}': {e}")
        raise

def go_back_to_list():
    """Click the back arrow to return to the ticket/lead list."""
    try:
        back_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']"))
        )
        back_btn.click()
        print("✅ Navigated back to list page")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Back navigation failed: {e}")

def close_modal():
    """Try multiple close button strategies."""
    for xpath in ["//button[@aria-label='Close']", "//span[@aria-label='close']"]:
        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            close_btn.click()
            print("✅ Modal closed")
            time.sleep(3)
            return
        except Exception:
            continue
    print("⚠️ Could not find close button for modal")

def select_advising_doctor():
    """Select the first advising doctor from dropdown."""
    try:
        advising_doctor = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-row ant-row-middle']//div[@class='ant-select-selector']")
            )
        )
        advising_doctor.click()
        print("✅ Advising doctor dropdown clicked")
        time.sleep(3)

        first_doctor = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-item-option-content')]")
            )
        )
        first_doctor.click()
        print("✅ First advising doctor selected")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Advising doctor selection failed: {e}")

def click_dropdown_and_select_patient():
    """Open patient dropdown and select the first patient."""
    try:
        dropdown_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']")
            )
        )
        dropdown_input.click()
        print("✅ Patient dropdown opened")
        time.sleep(5)

        patient = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]")
            )
        )
        patient.click()
        print("✅ First patient selected")
        time.sleep(5)
        return True

    except Exception as e:
        print(f"❌ Patient dropdown selection failed: {e}")
        return False

def click_add_more_services():
    """Click Add More Services button. Returns True if successful, False otherwise."""
    try:
        short_wait = WebDriverWait(driver, 5)  # Use 5-second timeout instead of 30
        add_more = short_wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-lg ant-btn-block crm-outline-btn']")
            )
        )
        add_more.click()
        print("✅ Add More Services clicked")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"⚠️ Add More Services not available (page state issue): {e}")
        return False

# ══════════════════════════════════════════════════════════════
#         TRANSACTION HISTORY FLOW
# ══════════════════════════════════════════════════════════════
def run_transaction_history_flow(context=""):
    print(f"\n{'─'*50}")
    print(f"🔄 Running Transaction History Flow [{context}]")
    print(f"{'─'*50}")

    if not click_dropdown_and_select_patient():
        print(f"⚠️ [{context}] Skipping transaction flow — patient selection failed")
        return False

    try:
        dot = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']")
            )
        )
        time.sleep(2)
        dot.click()
        print("✅ 3-dot menu clicked")
    except Exception as e:
        print(f"❌ [{context}] 3-dot menu not found — skipping history flow: {e}")
        return False

    try:
        history = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']")
            )
        )
        history.click()
        print("✅ History opened")
        time.sleep(3)
    except Exception as e:
        print(f"❌ [{context}] History button not found — skipping: {e}")
        return False

    try:
        payment_history = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]"))
        )
        payment_history.click()
        print("✅ Payment History tab clicked")
        time.sleep(7)
    except Exception as e:
        print(f"❌ [{context}] Payment History tab not found — skipping: {e}")
        close_modal()
        return False

    close_modal()
    return True

# ══════════════════════════════════════════════════════════════
#         COMMUNICATION HISTORY FLOW
# ══════════════════════════════════════════════════════════════
def run_communication_history_flow(context=""):
    print(f"\n🔄 Running Communication History Flow [{context}]")
    try:
        go_to_tab('Communication History')
        view_message = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]")
            )
        )
        view_message.click()
        print("✅ View Message opened")
        time.sleep(5)
        close_modal()
        time.sleep(3)
    except Exception as e:
        print(f"❌ [{context}] Communication History flow failed: {e}")

# ══════════════════════════════════════════════════════════════
#   FULL DETAIL FLOW: Transactions + Communication + Activity
# ══════════════════════════════════════════════════════════════
def run_full_detail_flow(context="", detail_tab_name="Ticket Details"):
    print(f"\n{'═'*55}")
    print(f"  FULL DETAIL FLOW — {context}")
    print(f"{'═'*55}")

    try:
        go_to_tab('Transactions')
    except Exception as e:
        print(f"❌ [{context}] Cannot open Transactions tab: {e}")
        go_back_to_list()
        return

    history_success = run_transaction_history_flow(context=context)
    if not history_success:
        print(f"⏭️ [{context}] Transaction History skipped — moving to Communication History")

    run_communication_history_flow(context=context)

    try:
        go_to_tab('Activity History')
    except Exception as e:
        print(f"❌ [{context}] Activity History tab failed: {e}")

    try:
        go_to_tab(detail_tab_name)
    except Exception as e:
        print(f"❌ [{context}] Could not return to {detail_tab_name}: {e}")

    go_back_to_list()

# ══════════════════════════════════════════════════════════════
#              TICKET STATUS FLOWS
# ══════════════════════════════════════════════════════════════
def run_ticket_tab(status_name, tab_xpath):
    print(f"\n{'━'*55}")
    print(f"  TICKET TAB → {status_name.upper()}")
    print(f"{'━'*55}")
    try:
        tab_btn = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
        tab_btn.click()
        print(f"✅ Switched to '{status_name}' tab")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Could not switch to '{status_name}' tab: {e}")
        return

    opened = open_first_row(row_type=f"{status_name} ticket")
    if not opened:
        return

    run_full_detail_flow(context=f"Ticket/{status_name}", detail_tab_name="Ticket Details")

def run_all_ticket_tabs():
    ticket_tabs = [
        ("Open",      "//span[normalize-space()='Open']"),
        ("Closed",    "//span[normalize-space()='Closed']"),
        ("Follow-up", "//span[normalize-space()='Follow-up']"),
        ("On-Hold",   "//span[normalize-space()='On-hold']"),
        ("Expired",   "//span[normalize-space()='Expired']"),
        ("Invalid",   "//span[normalize-space()='Invalid']"),
    ]
    for status_name, xpath in ticket_tabs:
        run_ticket_tab(status_name, xpath)

# ══════════════════════════════════════════════════════════════
#              LEAD STATUS FLOWS
# ══════════════════════════════════════════════════════════════
def navigate_to_leads():
    try:
        lead_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[@title='Leads']//*[name()='svg']"))
        )
        lead_icon.click()
        print("✅ Navigated to Leads section")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Could not navigate to Leads: {e}")
        raise

def run_lead_tab(status_name, tab_xpath):
    print(f"\n{'━'*55}")
    print(f"  LEAD TAB → {status_name.upper()}")
    print(f"{'━'*55}")
    try:
        tab_btn = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
        tab_btn.click()
        print(f"✅ Switched to '{status_name}' lead tab")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Could not switch to '{status_name}' lead tab: {e}")
        return

    opened = open_first_row(row_type=f"{status_name} lead")
    if not opened:
        return

    run_full_detail_flow(context=f"Lead/{status_name}", detail_tab_name="Lead Details")

def run_all_lead_tabs():
    lead_tabs = [
        ("New",       "//span[normalize-space()='New']"),
        ("Follow-up", "//span[normalize-space()='Follow-up']"),
        ("Converted", "//span[normalize-space()='Converted']"),
        ("Denied",    "//span[normalize-space()='Denied']"),
        ("Closed",    "//span[normalize-space()='Closed']"),
    ]
    for status_name, xpath in lead_tabs:
        run_lead_tab(status_name, xpath)

# ══════════════════════════════════════════════════════════════
#              TICKET REPORT DOWNLOAD FUNCTION
# ══════════════════════════════════════════════════════════════
def download_ticket_report(email):
    print("\n📥 Starting Ticket Report Download...")
    try:
        download_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='download']//*[name()='svg']"))
        )
        download_btn.click()
        print("✅ Download button clicked")
        time.sleep(5)

        start_day = (datetime.today() - timedelta(days=3)).day
        end_day = datetime.today().day
        print(f"📅 Date range: {start_day} → {end_day}")

        date_range_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body/div/div[@class='ant-modal-root']/div[@class='ant-modal-wrap ant-modal-centered']/div[@role='dialog']/div[@class='ant-modal-content']/div[@class='ant-modal-body']/form[@class='ant-form ant-form-horizontal crm-form']/div[2]/div[1]/div[2]")
            )
        )
        date_range_input.click()
        time.sleep(3)

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'ant-picker-dropdown')]")
        ))

        start_date = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"(//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{start_day}'])[1]")
            )
        )
        driver.execute_script("arguments[0].click();", start_date)
        print(f"✅ Start date selected: {start_day}")
        time.sleep(1)

        end_date = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"(//div[contains(@class,'ant-picker-panel')])[2]//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{end_day}']")
            )
        )
        end_date.click()
        print(f"✅ End date selected: {end_day}")
        time.sleep(2)

        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='email']")))
        email_field.clear()
        email_field.send_keys(Keys.CONTROL + "a")
        email_field.send_keys(Keys.DELETE)
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='email']")))
        email_field.send_keys(email)
        print(f"✅ Email entered: {email}")
        time.sleep(2)

        submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Submit']")))
        submit.click()
        print("✅ Report submitted — email will be sent")
        time.sleep(10)

    except Exception as e:
        print(f"❌ Report download failed: {e}")

# ══════════════════════════════════════════════════════════════
#              MORE FILTERS FUNCTION
# ══════════════════════════════════════════════════════════════
def apply_more_filters():
    """Open More Filters panel, click each filter, wait 15 sec for user to select, then move on."""
    print("\n🔧 Applying More Filters...")
    try:
        more_filter = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='More Filters']"))
        )
        more_filter.click()
        print("✅ More Filters panel opened")
        time.sleep(2)

        filter_xpaths = {
            "Agent":          "//*[@id='moreFilters']/div/div[1]/div/div/div[2]/div",
            "Branch":         "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
            "Ticket Type":    "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
            "Ticket SubType": "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
            "Category":       "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
            "Priority":       "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div[contains(@class,'ant-popover-content')]/div[contains(@role,'tooltip')]/div[contains(@class,'ant-popover-inner-content')]/form[@id='moreFilters']/div[contains(@class,'ant-row')]/div[6]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
            "Source":         "//input[@id='moreFilters_source_id']",
        }

        for filter_name, xpath in filter_xpaths.items():
            try:
                # ── Click the filter to open dropdown ──
                field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                field.click()
                print(f"✅ '{filter_name}' filter clicked")

                # ── Wait 30 seconds for user to manually select if needed ──
                print(f"⏳ Waiting 10 sec — select '{filter_name}' value or leave blank...")
                time.sleep(10)
                print(f"⏭️ Moving to next filter")

            except Exception as e:
                print(f"⚠️ '{filter_name}' filter skipped: {e}")

        # ── Close More Filters panel ──
        more_filter_close = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='More Filters']"))
        )
        driver.execute_script("arguments[0].click();", more_filter_close)
        print("✅ More Filters panel closed")
        time.sleep(5)

    except Exception as e:
        print(f"❌ More Filters flow failed: {e}")

# ══════════════════════════════════════════════════════════════
#              BOOKING FLOW 1 — CONSULTATION ✅
# ══════════════════════════════════════════════════════════════
def book_consultation():
    """Book a Doctor Consultation appointment."""
    print(f"\n{'─'*50}")
    print("📋 BOOKING FLOW → CONSULTATION")
    print(f"{'─'*50}")
    try:
        # ── Step 1: Click Doctor Consult ──
        consult = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Doctor Consult')]"))
        )
        driver.execute_script("arguments[0].click();", consult)
        print("✅ Doctor Consult service selected")
        time.sleep(5)

        # ── Step 2: All Bookings → New Booking ──
        all_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='All Bookings']"))
        )
        driver.execute_script("arguments[0].click();", all_booking)
        print("✅ All Bookings tab clicked")
        time.sleep(5)

        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        driver.execute_script("arguments[0].click();", new_booking)
        print("✅ New Booking tab clicked")
        time.sleep(5)

        # ── Step 3: Wait for booking page to fully load ──
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-selector']"))
        )
        print("✅ Booking page loaded")
        time.sleep(3)

        # ── Step 4: Select Region ──
        region_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
        )
        region_dropdown.click()
        print("✅ Region dropdown opened")
        time.sleep(3)

        first_region = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]")
            )
        )
        first_region.click()
        print("✅ First region selected")
        time.sleep(3)

        # ── Step 5: Select Hospital ──
        hospital_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
        )
        hospital_dropdown.click()
        print("✅ Hospital dropdown opened")
        time.sleep(3)

        all_hospitals = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]")
            )
        )
        all_hospitals.click()
        print("✅ All Hospitals/Clinics selected")
        time.sleep(3)

        # ── Step 6: Click Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        search_btn.click()
        print("✅ Search clicked")
        time.sleep(5)

        # ── Step 7: Earliest Availability ──
        earliest = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]")
            )
        )
        earliest.click()
        print("✅ Earliest availability clicked")
        time.sleep(5)

        # ── Step 8: Select Slot button ──
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
                slot_xpath = "(//div[contains(@class, 'slot-time')])[2]"
        
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

        # ── Step 10: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
            )
        )
        add_to_cart.click()
        print("✅ Add to cart clicked")
        time.sleep(3)

        # ── Step 11: Proceed to cart ──
        proceed_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]")
            )
        )
        proceed_to_cart.click()
        print("✅ Proceed to cart clicked")
        time.sleep(8)

        # ── Step 12: Edit slot ──
        edit_slots = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-row ant-row-end']//div[3]//*[name()='svg']")
            )
        )
        edit_slots.click()
        print("✅ Edit slots clicked")
        time.sleep(10)

        # ── Step 13: Re-select slot after edit ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 14: Add to cart after edit ──
        add_to_cart2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        add_to_cart2.click()
        print("✅ Add to cart (after edit) clicked")
        time.sleep(5)

        # ── Step 15: Proceed to cart after edit ──
        proceed_to_cart2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]")
            )
        )
        proceed_to_cart2.click()
        print("✅ Proceed to cart (after edit) clicked")
        time.sleep(10)

        print("✅✅ Consultation booking COMPLETED")

    except Exception as e:
        print(f"❌ Consultation booking failed: {e}")
        driver.save_screenshot("consultation_error.png")

# ══════════════════════════════════════════════════════════════
#              BOOKING FLOW 2 — RADIOLOGY ✅
# ══════════════════════════════════════════════════════════════
def book_radiology():
    """Book a Radiology (CT) appointment."""
    print(f"\n{'─'*50}")
    print("🏥 BOOKING FLOW → RADIOLOGY")
    print(f"{'─'*50}")
    try:
        # ── Step 1: Add More Services ──
        if not click_add_more_services():
            print("⚠️ Skipping Radiology booking due to page state issue")
            return

        # ── Step 2: Radiology/Other Diagnostic ──
        radiology_od = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-modal-body')]//div[2]//button[1]")
            )
        ) 
        radiology_od.click()
        print("✅ Radiology/Other Diagnostic selected")
        time.sleep(3)

        # ── Step 3: Radiology button ──
        radiology_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-row service-selection')]//div[1]//button[1]")
            )
        )
        radiology_btn.click()
        print("✅ Radiology button clicked")
        time.sleep(3)

        # ── Step 4: All Bookings → New Booking ──
        all_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='All Bookings']"))
        )
        all_booking.click()
        print("✅ All Bookings tab clicked")
        time.sleep(5)

        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        new_booking.click()
        print("✅ New Booking tab clicked")
        time.sleep(5)

        # ── Step 5: Wait for page to load ──
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-selector']"))
        )
        print("✅ Radiology booking page loaded")
        time.sleep(3)

        # ── Step 6: Select Region ──
        region_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
        )
        region_dropdown.click()
        print("✅ Region dropdown opened")
        time.sleep(3)

        first_region = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]")
            )
        )
        first_region.click()
        print("✅ First region selected")
        time.sleep(3)

        # ── Step 7: Select Hospital ──
        hospital_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
        )
        hospital_dropdown.click()
        print("✅ Hospital dropdown opened")
        time.sleep(3)

        all_hospitals = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]")
            )
        )
        all_hospitals.click()
        print("✅ All Hospitals/Clinics selected")
        time.sleep(3)

        # ── Step 8: Select Modality ──
        modality = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//span[@class='ant-select-selection-search'])[5]")
            )
        )
        modality.click()
        print("✅ Modality dropdown clicked")
        time.sleep(3)

        dropdown_container = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]")
            )
        )
        found = False
        for _ in range(10):
            try:
                option = driver.find_element(
                    By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='COMPUTERISED TOMOGRAPHY']"
                )
                driver.execute_script("arguments[0].click();", option)
                print("✅ COMPUTERISED TOMOGRAPHY selected")
                found = True
                break
            except Exception:
                driver.execute_script("arguments[0].scrollTop += 200", dropdown_container)
                time.sleep(1)
        if not found:
            print("❌ COMPUTERISED TOMOGRAPHY not found — skipping Radiology booking")
            return

        # ── Step 9: Select Test ──
        radiology_test = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[@class='ant-select-selector'])[6]")
            )
        )
        radiology_test.click()
        print("✅ Radiology Test dropdown clicked")
        time.sleep(3)

        dropdown_container = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]")
            )
        )
        found = False
        for _ in range(10):
            try:
                option = driver.find_element(
                    By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='CT ANGIOGRAPHY BRAIN']"
                )
                driver.execute_script("arguments[0].click();", option)
                print("✅ CT ANGIOGRAPHY BRAIN selected")
                found = True
                break
            except Exception:
                driver.execute_script("arguments[0].scrollTop += 200", dropdown_container)
                time.sleep(1)
        if not found:
            print("❌ CT ANGIOGRAPHY BRAIN not found — skipping")
            return

        # ── Step 10: Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        search_btn.click()
        print("✅ Search clicked for Radiology test")
        time.sleep(5)

        # ── Step 11: Earliest Availability ──
        earliest_availability = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]")
            )
        )
        earliest_availability.click()
        print("✅ Earliest availability clicked")
        time.sleep(5)

        # ── Step 12: Select Slot ──
        select_slot_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]")
            )
        )
        select_slot_btn.click()
        print("✅ Select Slot button clicked")
        time.sleep(7)

        # ── Step 13: First available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 14: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart)
        print("✅ Add to cart clicked")
        time.sleep(3)

        # ── Step 16: Edit slot ──
        edit_slots = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/*[name()='svg'][1]/*[name()='path'][1]")
            )
        )
        edit_slots.click()
        print("✅ Edit slots clicked")
        time.sleep(10)

        # ── Step 17: Re-select slot ──
        select_first_available_slot()
        time.sleep(3)

        # ── Step 18: Add to cart (after edit) ──
        add_to_cart_edit = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart_edit)
        print("✅ Add to cart (after edit) clicked")
        time.sleep(3)

        # ── Step 19: Proceed to cart (after edit) ──
        proceed_to_cart_edit = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]")
            )
        )
        proceed_to_cart_edit.click()
        print("✅ Proceed to cart (after edit) clicked")
        time.sleep(3)

        print("✅✅ Radiology booking COMPLETED")

        select_advising_doctor()
        time.sleep(3)

    except Exception as e:
        print(f"❌ Radiology booking failed: {e}")
        driver.save_screenshot("radiology_error.png")

# ══════════════════════════════════════════════════════════════
#              BOOKING FLOW 3 — LAB ✅
# ══════════════════════════════════════════════════════════════
def book_lab():
    """Book a Lab test appointment."""
    print(f"\n{'─'*50}")
    print("🧪 BOOKING FLOW → LAB")
    print(f"{'─'*50}")
    try:
        # ── Step 1: Add More Services → Lab ──
        if not click_add_more_services():
            print("⚠️ Skipping Lab booking—'Add More Services' not available")
            return

        lab_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Lab')]"))
        )
        lab_btn.click()
        print("✅ Lab button clicked")
        time.sleep(3)

        # ── Step 2: Lab @ Hospital ──
        lab_hospital = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Hospital')]"))
        )
        lab_hospital.click()
        print("✅ Lab @ Hospital selected")
        time.sleep(3)

        # ── Step 3: Select specific hospital ──
        select_hospital = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-lg')]//div[@class='ant-select-selector']")
            )
        )
        select_hospital.click()
        print("✅ Hospital selector clicked")
        time.sleep(3)

        first_lab_hospital = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(),'Medanta Hospital, Gurugram')]")
            )
        )
        first_lab_hospital.click()
        print(f"✅ Hospital selected: {first_lab_hospital.text}")
        time.sleep(5)

        # ── Step 4: Continue ──
        continue_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
        )
        continue_btn.click()
        print("✅ Continue clicked")
        time.sleep(3)

        # ── Step 5: All Bookings → New Booking ──
        all_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='All Bookings']"))
        )
        all_booking.click()
        print("✅ All Bookings tab clicked")
        time.sleep(5)

        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        new_booking.click()
        print("✅ New Booking tab clicked")
        time.sleep(5)

        # ── Step 6: Wait for lab page to load ──
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        print("✅ Lab booking page loaded")
        time.sleep(3)

        # ── Step 7: Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        search_btn.click()
        print("✅ Search clicked")
        time.sleep(5)

        # ── Step 8: Add first test to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//span[contains(text(),'Add To Cart')])[1]")
            )
        )
        add_to_cart.click()
        print("✅ First lab test added to cart")
        time.sleep(10)

        # ── Step 9: Open cart ──
        cart_logo = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='anticon']//*[name()='svg']")
            )
        )
        cart_logo.click()
        print("✅ Cart opened")
        time.sleep(5)

        select_advising_doctor()
        time.sleep(3)

        # ── Step 11: Add more lab tests ──
        add_more_lab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-text text-primary p-0']")
            )
        )
        add_more_lab.click()
        print("✅ Add more lab tests clicked")
        time.sleep(5)

        # ── Step 12: Add second test to cart ──
        add_to_cart2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//span[contains(text(),'Add To Cart')])[2]")
            )
        )
        add_to_cart2.click()
        print("✅ Second lab test added to cart")
        time.sleep(10)

        # ── Step 13: Open cart again ──
        cart_logo2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='anticon']//*[name()='svg']")
            )
        )
        cart_logo2.click()
        print("✅ Cart opened again")
        time.sleep(5)

        # ── Step 14: Select slot ──
        select_slot_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-text']")
            )
        )
        select_slot_btn.click()
        print("✅ Select slot clicked")
        time.sleep(5)

        # ── Step 15: First available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 16: Continue after slot ──
        continue_btn2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        continue_btn2.click()
        print("✅ Continue after slot selection clicked")
        time.sleep(5)

        print("✅✅ Lab booking COMPLETED")

    except Exception as e:
        print(f"❌ Lab booking failed: {e}")
        driver.save_screenshot("lab_error.png")

# ══════════════════════════════════════════════════════════════
#              BOOKING FLOW 4 — EHC ✅
# ══════════════════════════════════════════════════════════════
def book_ehc():
    """Book an EHC appointment."""
    print(f"\n{'─'*50}")
    print("🏨 BOOKING FLOW → EHC")
    print(f"{'─'*50}")
    try:
        # ── Step 1: Add More Services ──
        click_add_more_services()

        # ── Step 2: Click EHC button ──
        ehc_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'EHC')]"))
        )
        ehc_btn.click()
        print("✅ EHC button clicked")
        time.sleep(3)

        # ── Step 3: All Bookings tab ──
        all_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='All Bookings']"))
        )
        all_booking.click()
        print("✅ All Bookings tab clicked")
        time.sleep(5)

        # ── Step 4: New Booking tab ──
        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        new_booking.click()
        print("✅ New Booking tab clicked")
        time.sleep(5)

        # ── Step 5: Wait for page to load ──
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-selector']"))
        )
        print("✅ EHC booking page loaded")
        time.sleep(3)

        # ── Step 6: Select Region ──
        region_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))
        )
        region_dropdown.click()
        print("✅ Region dropdown opened")
        time.sleep(3)

        first_region = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-item-option')][1]")
            )
        )
        first_region.click()
        print("✅ First region selected")
        time.sleep(3)

        # ── Step 7: Select Hospital ──
        hospital_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[3]"))
        )
        hospital_dropdown.click()
        print("✅ Hospital dropdown opened")
        time.sleep(3)

        all_hospitals = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]")
            )
        )
        all_hospitals.click()
        print("✅ All Hospitals/Clinics selected")
        time.sleep(3)

        # ── Step 8: Click Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        search_btn.click()
        print("✅ Search button clicked")
        time.sleep(5)

        # ── Step 9: Select earliest availability ──
        earliest_availability = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body//div[@id='root']//div[@class='ant-col ant-col-24']//div[@class='ant-col ant-col-24']//div[@class='ant-col ant-col-24']//div[1]//div[1]//div[1]//div[1]//div[1]//div[2]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//div[1]//button[1]//div[1]//div[3]//p[1]")
                #(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]")
            )
        )
        earliest_availability.click()
        print("✅ Earliest availability clicked")
        time.sleep(5)

        # ── Step 10: Select slot ──
        select_slot_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//body//div[@id='root']//div[@class='ant-col ant-col-24']//div[@class='ant-col ant-col-24']//div[@class='ant-col ant-col-24']//div[1]//div[1]//div[1]//div[1]//div[1]//div[2]//div[1]//div[2]//div[1]//div[1]//div[1]//div[2]//button[1]//span[1]")
                #(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]")
            )
        )
        select_slot_btn.click()
        print("✅ Select slot button clicked")
        time.sleep(7)

        # ── Step 11: First available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 12: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
            )
        )
        add_to_cart.click()
        print("✅ Add to cart clicked")
        time.sleep(3)

        print("✅✅ EHC booking COMPLETED")

        select_advising_doctor()
        time.sleep(3)

        # ── Step 14: Proceed to checkout/Book Now ──
        book_now = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Book Now']"))
        )
        driver.execute_script("arguments[0].click();", book_now)
        print("✅ Book Now clicked")
        time.sleep(3)

        # ── Step 15: Confirm Booking ──
        confirm_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Confirm Booking']"))
        )
        driver.execute_script("arguments[0].click();", confirm_booking)
        print("✅ Confirm Booking clicked")
        time.sleep(5)
        
        close_modal()
        time.sleep(3)

        print("✅✅ Complete Services have been booked for this lead")

    except Exception as e:
        print(f"❌ EHC booking failed: {e}")
        driver.save_screenshot("ehc_error.png")

# ══════════════════════════════════════════════════════════════
#         OPEN NEW LEAD AND RUN ALL BOOKING FLOWS
# ══════════════════════════════════════════════════════════════
def run_lead_booking_flows():
    """Navigate to Leads New tab → open first lead → run all 4 booking flows."""
    print(f"\n{'═'*55}")
    print("  LEAD BOOKING FLOWS (Consult + Radiology + Lab + EHC)")
    print(f"{'═'*55}")
    try:
        navigate_to_leads()
        time.sleep(3)

        new_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New']"))
        )
        new_tab.click()
        print("✅ Switched to New lead tab")
        time.sleep(5)

        opened = open_first_row(row_type="lead")
        if not opened:
            print("⚠️ No leads available for booking flows — skipping")
            return

        book_consultation()

        # Navigate back to lead detail page after consultation booking
        try:
            driver.back()
            time.sleep(5)
            print("✅ Navigated back to lead detail page")
        except Exception as e:
            print(f"⚠️ Could not navigate back: {e}")

        book_radiology()
        book_lab()
        book_ehc()

        print("\n✅ All 4 booking flows completed for this lead")

    except Exception as e:
        print(f"❌ Lead booking flows failed: {e}")
        driver.save_screenshot("lead_booking_error.png")

# ══════════════════════════════════════════════════════════════
#                     MAIN EXECUTION
# ══════════════════════════════════════════════════════════════
def main():
    try:
        # ── 1. Login ──
        login(
            url="https://uatmedi-crmui.medanta.org:5443/medanta/crm/login",
            mobile="7291075289",
            otp_digits=["3", "2", "1", "5", "6", "4"]
        )

        # ── 2. Clear Calendar & Run All TICKET Tabs ──
        clear_calendar_filter()
        run_all_ticket_tabs()

        # ── 3. Download Ticket Report ──
        download_ticket_report(email="rsingh@gmail.com")

        # ── 4. Apply More Filters ──
        apply_more_filters()

        # ── 5. Navigate to Leads & Run All LEAD Status Tabs ──
        navigate_to_leads()
        clear_calendar_filter()
        run_all_lead_tabs()

        # ── 6. Re-open Lead & Run All Booking Flows ──
        run_lead_booking_flows()

        print("\n\n✅✅✅  ALL FLOWS COMPLETED SUCCESSFULLY  ✅✅✅")

    except KeyboardInterrupt:
        print("\n⏹️ Script interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR in main flow: {e}")
        driver.save_screenshot("critical_error.png")

    finally:
        time.sleep(30)
        driver.quit()
        print("🔒 Browser closed")

if __name__ == "__main__":
    main()

