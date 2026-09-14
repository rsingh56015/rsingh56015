from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import options
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

sys.stdout.reconfigure(encoding='utf-8')

# ══════════════════════════════════════════════════════════════
#               OUTPUT CAPTURE SETUP (for PDF)
# ══════════════════════════════════════════════════════════════
class Tee:
    """Mirrors writes to both the real stdout and an internal buffer."""
    def __init__(self, real_stdout):
        self.real_stdout = real_stdout
        self.buffer = io.StringIO()

    def write(self, data):
        self.real_stdout.write(data)
        self.buffer.write(data)

    def flush(self):
        self.real_stdout.flush()

    def get_output(self):
        return self.buffer.getvalue()

    def reconfigure(self, **kwargs):
        """Stub to satisfy sys.stdout.reconfigure() calls."""
        pass

# Start capturing
_tee = Tee(sys.stdout)
sys.stdout = _tee


def save_output_to_pdf():
    """Save all captured console output to a timestamped PDF report."""
    output_text = _tee.get_output()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"CRM_Run_Report_{timestamp}.pdf"
    )

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, "CRM Selenium Script - Run Report", ln=True, align="C")
    pdf.set_font("Helvetica", size=9)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Output lines
    pdf.set_font("Courier", size=8)
    for line in output_text.splitlines():
        # Strip non-ascii characters (emoji, lines) to avoid FPDF encoding issues
        safe_line = line.encode('ascii', errors='replace').decode('ascii')
        # Strip control characters that FPDF cannot render
        safe_line = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', safe_line)
        pdf.multi_cell(0, 5, safe_line)

    pdf.output(pdf_path)
    # Write directly to real stdout so it shows even after redirect
    _tee.real_stdout.write(f"\n\ud83d\udcc4 PDF report saved: {pdf_path}\n")

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
#                RECOVERY & HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def recover_from_past_booking_error():
    """Detects 'Past Booking' error, closes modal, and re-schedules all services."""
    try:
        error_xpath = "//*[contains(text(), 'Slots for the some of the services cannot be booked')]"
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, error_xpath)))
            print("⚠️ Detected 'Slots for the some of the services cannot be booked error showing. Starting recovery...")
        except TimeoutException:
            return True 

        # Close Error Notification and Confirmation Modal
        try:
            driver.find_element(By.XPATH, "//span[@aria-label='close']").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[@class='ant-modal-close']").click()
            print("✅ Modals closed. Returning to cart to edit slots.")
            time.sleep(2)
        except:
            pass

        # Loop through all Edit (pencil) icons in the cart
        edit_icons_xpath = "//*[name()='svg' and @data-icon='edit']"
        edit_icons = driver.find_elements(By.XPATH, edit_icons_xpath)
        
        for i in range(len(edit_icons)):
            print(f"🔄 Re-scheduling Service #{i+1}...")
            current_icons = driver.find_elements(By.XPATH, edit_icons_xpath)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", current_icons[i])
            time.sleep(1)
            current_icons[i].click()
            time.sleep(4)

            # Select the 5th available slot for a safety buffer
            try:
                future_slot = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'slot-time')])[5]")))
                driver.execute_script("arguments[0].click();", future_slot)
                print(f"✅ Selected new future slot: {future_slot.text}")
            except:
                select_first_available_slot()

            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Update') or contains(., 'Add')]"))).click()
            time.sleep(3)

        # Final Retry
        print("🚀 Retrying final booking...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Book Now']"))).click()
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Confirm Booking']"))).click()
        return True
    except Exception as e:
        print(f"❌ Recovery failed: {e}")
        return False

def close_modal():
    for xpath in ["//button[@aria-label='Close']", "//span[@aria-label='close']", "//button[@class='ant-modal-close']"]:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            print("✅ Modal closed")
            time.sleep(2)
            return
        except:
            continue

# ══════════════════════════════════════════════════════════════
#              COMMON HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
def select_first_available_slot():
    """Selects the first available time slot."""
    try:
        print("🔍 Looking for available time slots...")
        first_slot = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'slot-time')])[2]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_slot)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", first_slot)
        selected_time = first_slot.text
        print(f"✅ Slot selected: {selected_time}")
        return True
    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select time slot: {e}")
        return False

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
        advising_dr_xpath = "//div[contains(text(),'Advising Dr.')]/following-sibling::div//div[contains(@class,'ant-select-selector')]"

        Advising_doctor = wait.until(
            EC.element_to_be_clickable((By.XPATH, advising_dr_xpath))
        )
        Advising_doctor.click()
        print("✅ Advising doctor dropdown is clicked successfully")
        time.sleep(3)

        first_doctor = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-item-option-content')]")
            )
        )
        first_doctor.click()
        print(f"✅ First advising doctor selected : {first_doctor.text}")
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
        print(f"✅ First patient selected : {patient.text}")
        time.sleep(10)
        return True

    except Exception as e:
        print(f"❌ Patient dropdown selection failed: {e}")
        return False

def click_add_more_services():
    """Click Add More Services button. Returns True if successful, False otherwise."""
    try:
        short_wait = WebDriverWait(driver, 8)
        add_more = short_wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Add More Services') or contains(@class,'crm-outline-btn')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_more)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", add_more)
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
        time.sleep(5)
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
    ]
    for status_name, xpath in lead_tabs:
        run_lead_tab(status_name, xpath)

# ══════════════════════════════════════════════════════════════
#              TICKET REPORT DOWNLOAD FUNCTION
# ══════════════════════════════════════════════════════════════
'''def download_ticket_report(email):
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
        print(f"❌ Report download failed: {e}")'''

# ══════════════════════════════════════════════════════════════
#              MORE FILTERS FUNCTION
# ══════════════════════════════════════════════════════════════
"""def apply_more_filters():
    
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
                time.sleep(2)

                # 2. Select the first value from the dropdown by default
                # This XPATH targets the first visible option in the active dropdown list
                first_option_xpath = "(//div[contains(@class, 'ant-select-item-option-content')])[1]"
                try:
                    first_value = wait.until(EC.element_to_be_clickable((By.XPATH, first_option_xpath)))
                    selected_text = first_value.text
                    first_value.click()
                    print(f"✅ Filter is selected {filter_name} and {selected_text} 1st option is selected")
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Could not select first value for '{filter_name}': {e}")

                # ── Wait 30 seconds for user to manually select if needed ──
                print(f"⏭️ Moving to next filter")
                time.sleep(3)

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
        print(f"❌ More Filters flow failed: {e}")"""

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
        time.sleep(7)

        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        driver.execute_script("arguments[0].click();", new_booking)
        print("✅ New Booking tab clicked")
        time.sleep(3)

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

        # ── Step 5b: Select Doctor (Dr Sanjay Mittal) ──
        try:
            print("🔍 Searching for Dr. Sanjay Mittal...")
            doc_input = None
            for xpath_query in [
                "//input[@placeholder='Select Doctor']",
                "//div[contains(@class,'ant-select') and (.//span[contains(text(),'Doctor')] or .//div[contains(text(),'Doctor')])]//input",
                "(//div[contains(@class,'ant-select-selector')])[5]//input",
                "(//div[contains(@class,'ant-select-selector')])[6]//input",
            ]:
                try:
                    doc_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xpath_query))
                    )
                    if doc_input:
                        break
                except Exception:
                    continue

            if doc_input:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", doc_input)
                time.sleep(1)
                driver.execute_script("arguments[0].focus();", doc_input)
                doc_input.click()
                time.sleep(1)
                doc_input.send_keys(Keys.CONTROL + "a")
                doc_input.send_keys(Keys.DELETE)
                time.sleep(0.5)
                doc_input.send_keys("Sanjay Mittal")
                print("✅ Entered 'Sanjay Mittal' in Doctor search field")
                time.sleep(2)

                # Look for dropdown option
                try:
                    option = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[contains(@class,'ant-select-item') and contains(.,'Sanjay Mittal')] | //div[contains(@class,'ant-select-dropdown')]//div[contains(text(),'Sanjay Mittal')]")
                        )
                    )
                    driver.execute_script("arguments[0].click();", option)
                    print("✅ Selected 'Dr Sanjay Mittal' from dropdown")
                    time.sleep(2)
                except Exception as opt_err:
                    print(f"⚠️ Direct option click: {opt_err}. Pressing ENTER on search input...")
                    doc_input.send_keys(Keys.RETURN)
                    time.sleep(2)
            else:
                print("⚠️ Trying fallback doctor dropdown click...")
                for selector_xpath in [
                    "//div[contains(@class,'ant-select') and (.//span[contains(text(),'Doctor')] or .//div[contains(text(),'Doctor')])]",
                    "(//div[@class='ant-select-selector'])[5]",
                    "(//div[@class='ant-select-selector'])[6]",
                ]:
                    try:
                        doc_dropdown = driver.find_element(By.XPATH, selector_xpath)
                        driver.execute_script("arguments[0].click();", doc_dropdown)
                        time.sleep(2)
                        active_input = driver.switch_to.active_element
                        active_input.send_keys("Sanjay Mittal")
                        time.sleep(2)
                        active_input.send_keys(Keys.RETURN)
                        print("✅ Fallback: Typed 'Sanjay Mittal' and pressed ENTER")
                        break
                    except Exception:
                        continue
        except Exception as doc_e:
            print(f"⚠️ Doctor selection notice: {doc_e}")

        # ── Step 6: Click Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Search clicked")
        time.sleep(5)

        # ── Step 7: Earliest Availability (if available & clickable) ──
        try:
            short_wait = WebDriverWait(driver, 4)
            earliest = short_wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(.,'Get Earliest Availability') and not(@disabled)]")
                )
            )
            driver.execute_script("arguments[0].click();", earliest)
            print("✅ Earliest availability clicked")
            time.sleep(10)
        except Exception:
            print("⏭️ Earliest availability not needed or disabled, proceeding to Select Slot")

        # ── Step 8: Select Slot button ──
        select_slot = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(.,'Select Slot')])[1]")
            )
        )
        driver.execute_script("arguments[0].click();", select_slot)
        print("✅ Select slot button is clicked successfully")
        time.sleep(7)

        # ── Step 9: Select available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 10: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button'] | //button[contains(.,'Add To Cart') or contains(.,'Add to Cart')]")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart)
        print("✅ Add to cart clicked")
        time.sleep(3)

        # ── Step 11: Proceed to cart ──
        proceed_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )
        driver.execute_script("arguments[0].click();", proceed_to_cart)
        print("✅ Proceed to cart clicked")
        time.sleep(8)

        # ── Step 12: Edit slot (Optional verify) ──
        '''try:
            edit_slots = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='ant-row ant-row-end']//div[3]//*[name()='svg']")
                )
            )
            driver.execute_script("arguments[0].click();", edit_slots)
            print("✅ Edit slots clicked")
            time.sleep(8)

            # Re-select slot after edit
            select_first_available_slot()
            time.sleep(2)

            # Add to cart after edit
            add_to_cart2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg'] | //button[contains(.,'Add To Cart') or contains(.,'Add to Cart')]")
                )
            )
            driver.execute_script("arguments[0].click();", add_to_cart2)
            print("✅ Add to cart (after edit) clicked")
            time.sleep(5)

            # Proceed to cart after edit
            proceed_to_cart2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@type,'submit')]")
                )
            )
            driver.execute_script("arguments[0].click();", proceed_to_cart2)
            print("✅ Proceed to cart (after edit) clicked")
            time.sleep(8)
        except Exception as edit_e:
            print(f"⏭️ Edit slot flow skipped/not needed: {edit_e}")'''

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
                (By.XPATH, "//div[contains(@class,'ant-modal-body')]//div[2]//button[1] | //button[contains(.,'Radiology') or contains(.,'Diagnostic')]")
            )
        ) 
        driver.execute_script("arguments[0].click();", radiology_od)
        print("✅ Radiology/Other Diagnostic selected")
        time.sleep(3)

        # ── Step 3: Radiology button ──
        radiology_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-row service-selection')]//div[1]//button[1] | //button[normalize-space()='Radiology']")
            )
        )
        driver.execute_script("arguments[0].click();", radiology_btn)
        print("✅ Radiology button clicked")
        time.sleep(3)

        # ── Step 4: All Bookings → New Booking ──
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
                (By.XPATH, "(//span[@class='ant-select-selection-search'])[5] | (//div[@class='ant-select-selector'])[5]")
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
        Radiologytest = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))
        )
        Radiologytest.click()
        print("✅ Radiology test dropdown is clicked successfully")
        time.sleep(1)

        # Real typeable input is nested INSIDE the selector div (Ant Design pattern)
        search_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@class='ant-select-selector'])[6]//input")
            )
        )

        search_input.send_keys("CT Angiography Brain")
        time.sleep(2)

        # Try to select the matching option, with scroll retry if not immediately visible
        found = False
        option_xpath = "//div[contains(@class,'ant-select-item-option-content') and contains(text(),'CT Angio') and contains(text(),'Brain')]"

        
        try:
            option = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
            time.sleep(0.5)
            #driver.execute_script("arguments[0].scrollIntoView(true);", option)
            driver.execute_script("arguments[0].click();", option)
            print("✅ CT ANGIOGRAPHY BRAIN selected")
            found = True
            #break
        except Exception:
            print("⚠️ Direct click failed/timed out. Attempting Keyboard Navigation fallback...")
            search_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            search_input.send_keys(Keys.ENTER)
            print("✅ CT ANGIOGRAPHY BRAIN selected via Keyboard Enter")
            # Scroll the dropdown list down and retry
           
        # ── Step 10: Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Search clicked for Radiology test")
        time.sleep(5)

        # ── Step 11: Earliest Availability (Optional/if available) ──
        try:
            short_wait = WebDriverWait(driver, 4)
            earliest_availability = short_wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(.,'Get Earliest Availability') and not(@disabled)]")
                )
            )
            driver.execute_script("arguments[0].click();", earliest_availability)
            print("✅ Earliest availability clicked")
            time.sleep(5)
        except Exception:
            print("⏭️ Earliest availability not needed or disabled, proceeding to Select Slot")

        # ── Step 12: Select Slot ──
        select_slot_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(., 'Select Slot')])[1]")
            )
        )
        driver.execute_script("arguments[0].click();", select_slot_btn)
        print("✅ Select Slot button clicked")
        time.sleep(7)

        # ── Step 13: First available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 14: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button'] | //button[contains(.,'Add To Cart') or contains(.,'Add to Cart')]")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart)
        print("✅ Add to cart clicked")
        time.sleep(3)

        select_advising_doctor()
        time.sleep(3)

        # ── Step 16: Edit slot (Optional) ──
        '''try:
            edit_slots = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[3]//div[1]//div[1]//div[3]//div[2]//div[1]//div[1]//div[2]//div[1]//div[2]//div[3]//*[name()='svg']//*[name()='path' and contains(@d,'M0.891602 ')] | //*[contains(@class,'edit-slot')]")
                )
            )
            driver.execute_script("arguments[0].click();", edit_slots)
            print("✅ Edit slots clicked")
            time.sleep(8)

            # Re-select slot
            select_first_available_slot()
            time.sleep(3)

            # Add to cart (after edit)
            add_to_cart_edit = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button'] | //button[contains(.,'Add To Cart') or contains(.,'Add to Cart')]")
                )
            )
            driver.execute_script("arguments[0].click();", add_to_cart_edit)
            print("✅ Add to cart (after edit) clicked")
            time.sleep(3)
        except Exception as edit_err:
            print(f"⏭️ Edit slot flow skipped/not needed: {edit_err}")'''

        print("✅✅ Radiology booking COMPLETED")

    except Exception as e:
        print(f"❌ Radiology booking failed: {e}")
        driver.save_screenshot("radiology_error.png")

# ══════════════════════════════════════════════════════════════
#              BOOKING FLOW 3 — LAB ✅
# ══════════════════════════════════════════════════════════════
'''def book_lab():
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
        driver.execute_script("arguments[0].click();", lab_btn)
        print("✅ Lab button clicked")
        time.sleep(3)

        # ── Step 2: Lab @ Hospital ──
        lab_hospital = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Hospital')] | //span[contains(., 'Hospital')]"))
        )
        driver.execute_script("arguments[0].click();", lab_hospital)
        print("✅ Lab @ Hospital selected")
        time.sleep(3)

        # ── Step 3: Select specific hospital ──
        select_hospital = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'ant-select-lg')]//div[@class='ant-select-selector'] | (//div[@class='ant-select-selector'])[1]")
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
        driver.execute_script("arguments[0].click();", continue_btn)
        print("✅ Continue clicked")
        time.sleep(3)

        # ── Step 5: All Bookings → New Booking ──
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

        # ── Step 6: Wait for lab page to load ──
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg'] | //button[contains(.,'Search')]")
            )
        )
        print("✅ Lab booking page loaded")
        time.sleep(3)

        # ── Step 7: Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg'] | //button[contains(.,'Search')]")
            )
        )
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Search clicked")
        time.sleep(5)

        # ── Step 8: Add first test to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//span[contains(text(),'Add To Cart') or contains(text(),'Add to Cart')])[1]/ancestor::button | (//button[contains(.,'Add To Cart') or contains(.,'Add to Cart')])[1]")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart)
        print("✅ First lab test added to cart")
        time.sleep(8)

        # ── Step 9: Open cart ──
        cart_logo = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='anticon']//*[name()='svg'] | //span[@aria-label='shopping-cart'] | //button[contains(@class,'cart')]")
            )
        )
        driver.execute_script("arguments[0].click();", cart_logo)
        print("✅ Cart opened")
        time.sleep(5)

        select_advising_doctor()
        time.sleep(3)

        # ── Step 11: Add more lab tests ──
        try:
            add_more_lab = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='ant-btn ant-btn-text text-primary p-0'] | //button[contains(.,'Add More Tests')]")
                )
            )
            driver.execute_script("arguments[0].click();", add_more_lab)
            print("✅ Add more lab tests clicked")
            time.sleep(5)

            # ── Step 12: Add second test to cart ──
            add_to_cart2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//span[contains(text(),'Add To Cart') or contains(text(),'Add to Cart')])[2]/ancestor::button | (//button[contains(.,'Add To Cart') or contains(.,'Add to Cart')])[2]")
                )
            )
            driver.execute_script("arguments[0].click();", add_to_cart2)
            print("✅ Second lab test added to cart")
            time.sleep(8)

            # ── Step 13: Open cart again ──
            cart_logo2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='anticon']//*[name()='svg'] | //span[@aria-label='shopping-cart']")
                )
            )
            driver.execute_script("arguments[0].click();", cart_logo2)
            print("✅ Cart opened again")
            time.sleep(5)
        except Exception as add_err:
            print(f"⏭️ Add second lab test step skipped/not applicable: {add_err}")

        # ── Step 14: Select slot ──
        try:
            select_slot_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='ant-btn ant-btn-text'] | (//button[contains(.,'Select Slot')])[1]")
                )
            )
            driver.execute_script("arguments[0].click();", select_slot_btn)
            print("✅ Select slot clicked")
            time.sleep(5)

            # ── Step 15: First available slot ──
            select_first_available_slot()
            time.sleep(2)

            # ── Step 16: Continue after slot ──
            continue_btn2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg'] | //button[contains(.,'Continue')]")
                )
            )
            driver.execute_script("arguments[0].click();", continue_btn2)
            print("✅ Continue after slot selection clicked")
            time.sleep(5)
        except Exception as slot_err:
            print(f"⏭️ Slot selection for Lab skipped/not applicable: {slot_err}")

        print("✅✅ Lab booking COMPLETED")

    except Exception as e:
        print(f"❌ Lab booking failed: {e}")
        driver.save_screenshot("lab_error.png")
'''
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
        if not click_add_more_services():
            print("⚠️ Skipping EHC booking due to page state issue")
            return

        # ── Step 2: Click EHC button ──
        ehc_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'EHC')]"))
        )
        driver.execute_script("arguments[0].click();", ehc_btn)
        print("✅ EHC button clicked")
        time.sleep(3)

        # ── Step 3: All Bookings tab ──
        all_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='All Bookings']"))
        )
        driver.execute_script("arguments[0].click();", all_booking)
        print("✅ All Bookings tab clicked")
        time.sleep(5)

        # ── Step 4: New Booking tab ──
        new_booking = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='New Booking']"))
        )
        driver.execute_script("arguments[0].click();", new_booking)
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

        EHCtest = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))
        )
        EHCtest.click()
        print("✅ EHC test dropdown is clicked successfully")
        time.sleep(1)

        # Real typeable input is nested INSIDE the selector div (Ant Design pattern)
        search_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@class='ant-select-selector'])[6]//input")
            )
        )

        search_input.send_keys("Medanta Basic Health Check")
        time.sleep(2)

        # Try to select the matching option, with scroll retry if not immediately visible
        found = False
        option_xpath = "//div[contains(@class,'ant-select-item-option-content') and contains(text(),'Medanta Basic') and contains(text(),'Health Check')]"

        
        try:
            option = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
            time.sleep(0.5)
            #driver.execute_script("arguments[0].scrollIntoView(true);", option)
            driver.execute_script("arguments[0].click();", option)
            print("✅ CT ANGIOGRAPHY BRAIN selected")
            found = True
            #break
        except Exception:
            print("⚠️ Direct click failed/timed out. Attempting Keyboard Navigation fallback...")
            search_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            search_input.send_keys(Keys.ENTER)
            print("✅ Medanta Basic Health Check selected via Keyboard Enter")
            # Scroll the dropdown list down and retry

        if not found:
            print("❌ Medanta Basic Health Check not found in dropdown")

        # ── Step 8: Click Search ──
        search_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
            )
        )
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Search button clicked")
        time.sleep(5)

        # ── Step 9: Select earliest availability (Optional/if available) ──
        try:
            short_wait = WebDriverWait(driver, 4)
            earliest_availability = short_wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Get Earliest Availability') and not(@disabled)]")
                )
            )
            driver.execute_script("arguments[0].click();", earliest_availability)
            print("✅ Earliest availability clicked")
            time.sleep(5)
        except Exception:
            print("⏭️ Earliest availability not needed or disabled, proceeding to Select Slot")

        # ── Step 10: Select slot ──
        select_slot_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(., 'Select Slot')])[1]")
            )
        )
        driver.execute_script("arguments[0].click();", select_slot_btn)
        print("✅ Select slot button clicked")
        time.sleep(7)

        # ── Step 11: First available slot ──
        select_first_available_slot()
        time.sleep(2)

        # ── Step 12: Add to cart ──
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button'] | //button[contains(.,'Add To Cart') or contains(.,'Add to Cart')]")
            )
        )
        driver.execute_script("arguments[0].click();", add_to_cart)
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

        # Sequentially run all 4 booking flows in the same cart
        book_consultation()
        book_radiology()
        #book_lab()
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
            url="https://betamedi-crmui.medanta.org:5443/medanta/crm/login",
            mobile="7011209294",
            otp_digits=["3", "2", "1", "5", "6", "4"]
        )
        time.sleep(15)

        # ── 2. Clear Calendar & Run All TICKET Tabs ──
        clear_calendar_filter()
        run_all_ticket_tabs()

        # ── 3. Download Ticket Report ──
        '''download_ticket_report(email="rsingh@medanta.org")'''

        # ── 4. Apply More Filters ──
        """apply_more_filters()"""

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

#============================================================================================
                        #PAYMENT FLOW
#============================================================================================
def paymentflow():
    """ doing the payment using card or upi."""
    print(f"\n{'─'*50}")
    print("📋 Payment Flow-All Services")
    print(f"{'─'*50}")
    
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
        link =  wait.until(
            EC.element_to_be_clickable(By.XPATH,"(//a[contains(text(),'http://medantabeta-medi-ui.hlthclub.in/MEDNTA/r/u/')])[1]")
        ).get_attribute("href")
        print("✅Payment link found")
        time.sleep(3)
        driver.get(link)
        time.sleep(10)
        
        
    except Exception as e:
        print(f"❌ Payment Flow failed: {e}")





    finally:
        time.sleep(30)
        save_output_to_pdf()
        driver.quit()
        print("🔒 Browser closed")

if __name__ == "__main__":
    main()

