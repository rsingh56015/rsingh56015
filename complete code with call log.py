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
        self.real_stdout.flush()
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

EMOJI_MAP = {
    "✅": "[OK]",
    "❌": "[FAIL]",
    "⚠️": "[WARN]",
    "⚠": "[WARN]",
    "🔒": "[LOCK]",
    "📄": "[PDF]",
    "👉": "->",
    "🎉": "[SUCCESS]",
    "🔍": "[SEARCH]",
    "🆕": "[NEW]",
}


def replace_emoji(text):
    for emoji, tag in EMOJI_MAP.items():
        text = text.replace(emoji, tag)
    return text

def save_output_to_pdf():
    """Save all captured console output to both timestamped .txt and .pdf reports."""
    try:
        output_text = _tee.get_output()
        if not output_text.strip():
            _tee.real_stdout.write("\n⚠️ No output captured for report.\n")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"CRM_Run_Report_{timestamp}.txt"
        )
        pdf_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"CRM_Run_Report_{timestamp}.pdf"
        )

        # 1. Save Full UTF-8 Plaintext Report (.txt)
        with open(txt_path, 'w', encoding='utf-8') as text_file:
            text_file.write(output_text)
        _tee.real_stdout.write(f"\n📄 TXT report saved: {txt_path}\n")

        # 2. Save PDF Report (.pdf)
        pdf = FPDF(format='A4')
        pdf.set_margins(10, 10, 10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        left_margin = pdf.l_margin
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin

        # Title
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.set_x(left_margin)
        pdf.cell(usable_width, 10, "CRM Selenium Script - Run Report",
                 align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", size=9)
        pdf.set_x(left_margin)
        pdf.cell(usable_width, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                 align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        # Output lines
        pdf.set_font("Courier", size=8)
        MAX_CHARS_PER_LINE = 110

        for line in output_text.splitlines():
            safe_line = replace_emoji(line)
            safe_line = safe_line.encode('ascii', errors='replace').decode('ascii')
            safe_line = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', safe_line)

            if not safe_line.strip():
                pdf.ln(4)
                continue

            wrapped_lines = textwrap.wrap(
                safe_line,
                width=MAX_CHARS_PER_LINE,
                break_long_words=True,
                break_on_hyphens=False
            ) or [""]

            for wrapped in wrapped_lines:
                try:
                    pdf.set_x(left_margin)
                    pdf.cell(usable_width, 5, text=wrapped,
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                except Exception:
                    pdf.set_x(left_margin)
                    pdf.cell(usable_width, 5, text="[unrenderable line skipped]",
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(pdf_path)
        _tee.real_stdout.write(f"📄 PDF report saved: {pdf_path}\n")
    except Exception as e:
        _tee.real_stdout.write(f"\n⚠️ Failed to save report: {e}\n")
# ══════════════════════════════════════════════════════════════════
#                        BROWSER SETUP
# ══════════════════════════════════════════════════════════════════
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")          # required: no display on GitHub's servers
    options.add_argument("--no-sandbox")             # required in CI containers
    options.add_argument("--disable-dev-shm-usage")  # avoids crashes from low shared memory
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # replaces --start-maximized for headless
    options.add_argument("--force-device-scale-factor=0.80")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.execute_script("document.body.style.zoom='80%'")
    return driver

driver = setup_driver()
wait = WebDriverWait(driver, 30)

# ══════════════════════════════════════════════════════════════════
#                        LOGIN
# ══════════════════════════════════════════════════════════════════

def login(driver, wait, url, mobile, otp_digits):
    driver.get(url)
    print(driver.title)

    mobile_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='number-login_username']")
    ))
    mobile_input.send_keys(mobile)
    print(f"✅ Mobile number {mobile} entered")

    get_otp_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Get OTP']/ancestor::button")
    ))
    get_otp_btn.click()
    print("✅ OTP page opened")
    time.sleep(3)

    for i, digit in enumerate(otp_digits, 1):
        otp_field = wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div/div/div/div/input[{i}]")
        ))
        otp_field.send_keys(digit)

    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div/form/div[3]/div/button")
    ))
    submit_btn.click()
    print("✅ Login Successful")
    time.sleep(15)

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

'''def closed_modal():
    for xpath in ["//button[@aria-label='Close']", "//span[@aria-label='close']", "//button[@class='ant-modal-close']", "//button[@class='ant-drawer-close']"]:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            print("✅ Modal closed")
            time.sleep(2)
            return
        except:
            continue'''
# ══════════════════════════════════════════════════════════════════
#                     COMMON HELPERS
# ══════════════════════════════════════════════════════════════════

def clear_date_filter(driver, wait, calendar_xpath, clear_btn_xpath):
    calendar = wait.until(EC.element_to_be_clickable((By.XPATH, calendar_xpath)))
    calendar.click()
    print("✅ Calendar clicked")
    time.sleep(2)
    try:
        remove_date = wait.until(EC.element_to_be_clickable((By.XPATH, clear_btn_xpath)))
        remove_date.click()
        print("✅ Date filter cleared")
    except Exception:
        print("⏭️ No date filter to clear, skipping...")
    time.sleep(5)

def get_table_rows(driver, wait):
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    ))
    time.sleep(2)
    rows = driver.find_elements(
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]/tr[not(contains(@class, 'ant-table-measure-row')) and not(@aria-hidden='true') and not(contains(@class, 'ant-table-placeholder'))]"
    )
    print(f"🔍 Rows found")
    return rows

def open_first_row(driver, rows, label="ticket"):
    total_count = len(rows)
    try:
        active_tab = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'ant-tabs-tab-active')]//div[contains(@class,'ant-tabs-tab-btn')] | //div[contains(@class,'ant-tabs-tab-active')] | //div[@role='tab' and @aria-selected='true']"
            ))
        )
        tab_name = active_tab.text.strip()
        print(f"📌 {tab_name} {label.capitalize()}s Count: {tab_name}")
    except Exception as e:
        print(f"⚠️ Could not fetch tab count: {e}")
    time.sleep(2)
    if total_count == 0:
        print(f"⚠️ No {label}s available to open")
        return False
    # Get first lead
    first_item = rows[0].find_element(By.XPATH,".//a[contains(@class,'bold-600')]")
    # Get complete text
    first_lead_text = first_item.text.strip()
    print(f"👤 1st {label.capitalize()} Patient Details:")
    print(first_lead_text)
    # Get only patient name
    patient_name = first_lead_text.split("(")[0].strip()
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_item)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", first_item)
    print(f"✅ 1st {label} opened successfully")
    time.sleep(5)
    return True

def click_tab(wait, tab_text):
    tab = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(text(),'{tab_text}')]")
    ))
    tab.click()
    print(f"✅ Navigated to '{tab_text}' tab")
    time.sleep(3)

def go_back_to_list(wait):
    back_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']")
    ))
    back_btn.click()
    print("✅ Navigated back to list page")
    time.sleep(5)

def close_modal(wait):
    close_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@aria-label='Close']")
    ))
    close_btn.click()
    print("✅ Modal closed")
    time.sleep(2)

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

# ══════════════════════════════════════════════════════════════════
#                  TRANSACTION TAB ACTIONS
# ══════════════════════════════════════════════════════════════════

def handle_transaction_tab(driver, wait):
    click_tab(wait, "Transactions")

    dropdown_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//div[@class='ant-select ant-select-single ant-select-allow-clear ant-select-show-arrow ant-select-show-search']")
    ))
    dropdown_input.click()
    print("✅ Patient dropdown opened")
    time.sleep(3)

    patient_list = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'rc-virtual-list-holder-inner')]"
        "//div[contains(@class,'ant-select-item-option')]"
    )
    print(f"📋Associated lead : Total contacts: {len(patient_list)}")

    try:
        patient = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'ant-select-item ant-select-item-option capitalize ant-select-item-option-active')]//div[contains(@class,'ant-select-item-option-content')]//div[1]")
        ))
        time.sleep(2)
        patient.click()
        print("✅ First patient selected")
        print(f"📋 Patient Name: {patient.text.strip()}")
        time.sleep(2)

        dot = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[1]//div[1]//div[4]//div[1]//div[1]//span[1]//*[name()='svg']")
        ))
        time.sleep(2)
        dot.click()
        print("✅User click on 3dot to view the history of the appointment")

        history = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'ant-dropdown ant-dropdown-placement-bottomRight')]//span[contains(@class,'ant-dropdown-menu-title-content')][normalize-space()='History']")
        ))
        history.click()
        print("✅History of this transaction has been open")
        time.sleep(3)

        payment_history = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[contains(@class,'ant-tabs-tab')])[15]")
        ))
        payment_history.click()
        print("✅Hisotry of this transaction has been open and Patient Journey is visibile")
        time.sleep(7)

        close_modal(wait)
        print("✅History section closed")

    except Exception as e:
        print(f"⚠️ Transaction tab error: {e}")
        print("⏭️ Skipping transaction interaction...")
        time.sleep(2)

# ══════════════════════════════════════════════════════════════════
#               COMMUNICATION HISTORY TAB ACTIONS
# ══════════════════════════════════════════════════════════════════

def handle_communication_history(driver, wait):
    click_tab(wait, "Communication History")

    view_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]")
    ))
    view_message.click()
    print("✅View message button is working fine and user able to view the last sms")
    time.sleep(5)

    try:
        message_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'ant-modal-content')]"))
        )
        print(f"📩 Complete SMS Message: {message_element.text.strip()}")
        time.sleep(2)
    except Exception:
        pass

    close_modal(wait)
    print("✅Message is now close and come back to the communication page")
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#              FULL TICKET/LEAD DETAIL FLOW
# ══════════════════════════════════════════════════════════════════

def handle_ticket_detail_flow(driver, wait, detail_tab_text="Ticket Details"):
    handle_transaction_tab(driver, wait)
    handle_communication_history(driver, wait)

    click_tab(wait, "Activity History")
    time.sleep(5)

    click_tab(wait, detail_tab_text)
    time.sleep(5)

    go_back_to_list(wait)

# ══════════════════════════════════════════════════════════════════
#            TICKET : NAVIGATE TO STATUS TAB AND PROCESS FIRST ITEM
# ══════════════════════════════════════════════════════════════════

def process_status_tab(driver, wait, tab_span_text, item_label="ticket", detail_tab_text="Ticket Details"):
    tab = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[normalize-space()='{tab_span_text}']")
    ))
    tab.click()
    print(f"Navigated to '{tab_span_text}' tab")
    time.sleep(5)

    rows = get_table_rows(driver, wait)

    if not open_first_row(driver, rows, label=item_label):
        return

    handle_ticket_detail_flow(driver, wait, detail_tab_text=detail_tab_text)
    print(f"✅ '{tab_span_text}' tab flow complete")

# ══════════════════════════════════════════════════════════════════
#                    MORE FILTERS
# ══════════════════════════════════════════════════════════════════

def apply_more_filters(driver, wait):
    more_filter = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='More Filters']")
    ))
    more_filter.click()
    print("More Filters opened")
    time.sleep(2)

    filter_xpaths = {
        "Agent":           "//*[@id='moreFilters']/div/div[1]/div/div/div[2]/div",
        "Branch":          "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
        "Ticket Type":     "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
        "Ticket Sub Type": "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
        "Category":        "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
        "Priority":        "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[6]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
        "Source":          "//body/div/div/div[contains(@class,'ant-popover ant-popover-placement-bottom')]/div/div/div/form[@id='moreFilters']/div/div[7]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]",
    }

    for name, xpath in filter_xpaths.items():
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            field.click()
            print(f"'{name}' filter clicked — any selection or blank is acceptable")
        except Exception as e:
            print(f"⚠️ Could not click '{name}' filter: {e}")
        time.sleep(2)

    more_filter_close = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='More Filters']")
    ))
    js_click(driver, more_filter_close)
    print("More Filters closed")
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#                    DOWNLOAD TICKET REPORT
# ══════════════════════════════════════════════════════════════════

def download_ticket_report(driver, wait, email):
    download = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='download']//*[name()='svg']")
    ))
    download.click()
    print("Download button clicked")
    time.sleep(10)

    ticket_reports = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@value='ticket_report']")
    ))
    print(f"Report Type: {ticket_reports.get_attribute('value')}")

    start_day = (datetime.today() - timedelta(days=3)).day
    end_day = datetime.today().day
    print(f"Date range: Start={start_day}, End={end_day}")

    date_range_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//body/div/div[@class='ant-modal-root']/div[@class='ant-modal-wrap ant-modal-centered']/div[@role='dialog']/div[@class='ant-modal-content']/div[@class='ant-modal-body']/form[@class='ant-form ant-form-horizontal crm-form']/div[2]/div[1]/div[2]")
    ))
    date_range_input.click()
    time.sleep(5)

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'ant-picker-dropdown')]")
    ))

    start_date = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"(//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{start_day}'])[1]")
    ))
    js_click(driver, start_date)
    print(f"✅ Start date selected: {start_day}")
    time.sleep(1)

    end_date = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"(//div[contains(@class,'ant-picker-panel')])[2]//td[contains(@class,'ant-picker-cell-in-view')]//div[text()='{end_day}']")
    ))
    time.sleep(3)
    end_date.click()
    print(f"✅ End date selected: {end_day}")
    time.sleep(2)

    email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='email']")))
    email_field.clear()
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(email)
    print(f"Email entered: {email}")
    time.sleep(3)

    submit = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Submit']")
    ))
    submit.click()
    print("✅ Report submitted — email will be sent")
    time.sleep(10)

# ══════════════════════════════════════════════════════════════════
#                    SLOT SELECTION HELPER
# ══════════════════════════════════════════════════════════════════

def select_first_available_slot(driver, wait):
    try:
        print("Looking for available time slots...")
        slot_xpath = "(//div[contains(@class, 'slot-time')])[4]"
        first_slot = wait.until(EC.element_to_be_clickable((By.XPATH, slot_xpath)))
        js_click(driver, first_slot)
        print(f"✅ Slot selected: {first_slot.text}")
    except Exception as e:
        driver.save_screenshot("slot_selection_error.png")
        print(f"❌ Failed to select slot: {e}")

# ══════════════════════════════════════════════════════════════════
#              CONSULT APPOINTMENT BOOKING
# ══════════════════════════════════════════════════════════════════

def book_consult_appointment(driver, wait, doctor_name="Sanjay Mittal"):
    consult = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(),'Doctor Consult')]")
    ))
    consult.click()
    print("✅Doctor Consult clicked")
    time.sleep(5)

    # All Bookings → New Booking
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='All Bookings']")
    )).click()
    print("✅All Bookings tab clicked")
    time.sleep(5)
    
    # New Booking
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='New Booking']")
    )).click()
    print("✅New Booking tab clicked")
    time.sleep(5)

    # Select Region
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[2]")
    )).click()
    print("✅Region dropdown clicked")
    time.sleep(3)
    Region = wait.until(EC.presence_of_element_located(
        (By.XPATH,
            "(//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden'))]"
            "//div[contains(@class,'ant-select-item-option')])[1]")
    ))
    region_name = Region.get_attribute("title") or Region.text.strip() or Region.get_attribute("innerText").strip()
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Region)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", Region)
    print(f"✅ Region selected : {region_name}")
    time.sleep(3)

    # Select Hospital
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[3]")
    )).click()
    print("✅ Hospital dropdown clicked")
    time.sleep(3)
    Hospital = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden'))]//div[contains(@class,'ant-select-item-option')])[1]")
    ))
    hospital_name = Hospital.get_attribute("title") or Hospital.text.strip() or Hospital.get_attribute("innerText").strip()
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Hospital)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", Hospital)
    print(f"✅ Hospital selected : {hospital_name}")
    time.sleep(3)

    # Select Doctor (if specified)
    Doctor = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))
    )
    Doctor.click()
    print("✅ Doctor dropdown is clicked successfully")
    time.sleep(1)

    # Real typeable input is nested INSIDE the selector div (Ant Design pattern)
    search_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "(//div[@class='ant-select-selector'])[6]//input")
        )
    )
    search_input.send_keys("Sanjay Mittal")
    print("Sanjay Mittal selected")
    time.sleep(2)

    # Try to select the matching option, with scroll retry if not immediately visible
    found = False
    option_xpath = "//div[contains(@class,'ant-select-item-option-content') and contains(text(),'Sanjay') and contains(text(),'Mittal')]"

    try:
        match = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        js_click(driver, match)
        found = True
        print(f"✅ Doctor selected: {match.text}")
    except Exception:
        print("⚠️ Direct click failed/timed out. Attempting Keyboard Navigation fallback...")
        search_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        print("✅ Sanjay Mittal selected via Keyboard Enter")
        # Scroll the dropdown list down and retry

    # Search
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
    )).click()
    print("Search clicked")
    time.sleep(5)

    # Earliest Availability
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Get Earliest Availability') and not(@disabled)]")
    )).click()
    print("✅ Earliest availability clicked")
    time.sleep(5)

    # Select Slot button
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//button[contains(.,'Select Slot')])[1]")
    )).click()
    print("✅ Select Slot clicked")
    time.sleep(5)
    close_modal(wait)

    # Select Slot button
    slot = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//button[contains(.,'Select Slot')])[1]")
    ))
    slot.click()
    print("✅ Select Slot clicked again for booking")
    time.sleep(7)

    select_first_available_slot(driver, wait)
    time.sleep(2)

    # Add to Cart
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
    )).click()
    print("✅ Add to cart clicked")
    time.sleep(3)

    # Proceed to Cart
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")
    )).click()
    print("✅ Proceed to cart clicked")
    time.sleep(8)

def edit_consult_slot(driver, wait):
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='ant-row ant-row-end']//div[3]//*[name()='svg']")
        )).click()
        print("✅ Edit slot clicked")
        time.sleep(10)

        select_first_available_slot(driver, wait)
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
        )).click()
        print("✅ Add to cart (re-edit) clicked")
        time.sleep(5)

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='ant-form-item-control-input-content'])[2]")
        )).click()
        print("✅ Proceed to cart (re-edit) clicked")
        time.sleep(5)
    except Exception as e:
        print(f"⚠️ Could not edit consult slot: {e}")
        print("⏭️ Skipping slot edit...")

# ══════════════════════════════════════════════════════════════════
#                    RADIOLOGY BOOKING
# ══════════════════════════════════════════════════════════════════

def book_radiology(driver, wait):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Add More Services') or contains(@class,'crm-outline-btn')]")
    )).click()
    print("✅ Add more services clicked")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-modal-body')]//div[2]//button[1]")
    )).click()
    print("✅ Radiology/Other Diagnostic clicked")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-row service-selection')]//div[1]//button[1]")
    )).click()
    print("✅ Radiology clicked")
    time.sleep(3)

    # All Bookings → New Booking
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='All Bookings']")
    )).click()
    print("✅All Bookings tab clicked")
    time.sleep(5)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='New Booking']")
    )).click()
    print("✅New Booking tab clicked")
    time.sleep(5)

    # Select Region
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[2]")
    )).click()
    print("Region dropdown clicked")
    time.sleep(3)
    Region = wait.until(EC.presence_of_element_located(
        (By.XPATH,
            "(//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden'))]"
            "//div[contains(@class,'ant-select-item-option')])[1]")
    ))
    region_name = Region.get_attribute("title") or Region.text.strip() or Region.get_attribute("innerText").strip()
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Region)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", Region)
    print(f"✅ Region selected : {region_name}")
    time.sleep(3)

    # Select Hospital
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[3]")
    )).click()
    print("Hospital dropdown clicked")
    time.sleep(3)

    Hospital = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden'))]//div[contains(@class,'ant-select-item-option')])[1]")
    ))
    hospital_name = Hospital.get_attribute("title") or Hospital.text.strip() or Hospital.get_attribute("innerText").strip()
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Hospital)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", Hospital)
    print(f"✅ Hospital selected : {hospital_name}")
    time.sleep(3)

    # Modality
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[@class='ant-select-selection-search'])[5]")
    )).click()
    print("Modality dropdown is clicked successfully")
    time.sleep(3)

    _select_dropdown_option(driver, wait, "COMPUTERISED TOMOGRAPHY")

    # Radiology Test
    Radiology_test = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[6]")
    ))
    Radiology_test.click()
    print("✅ Radiology test dropdown is clicked successfully")
    time.sleep(3)

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

    # Search
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
    )).click()
    print("Search button is clicked")
    time.sleep(5)

    # Earliest availability
    Earliest_availability = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Get Earliest Availability') and not(@disabled)]")
    ))
    Earliest_availability.click()
    print("✅ Earliest availability is clicked successfully")
    time.sleep(5)

    # Select Slot
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//button[contains(., 'Select Slot')])[1]")
    )).click()
    time.sleep(7)

    select_first_available_slot(driver, wait)
    time.sleep(2)

    # Add to cart
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
    )).click()
    time.sleep(4)
    print("✅ Radiology booked and added to cart")

def _select_dropdown_option(driver, wait, option_text):
    dropdown = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'rc-virtual-list-holder')]")
    ))
    found = False
    for _ in range(20):
        try:
            option = driver.find_element(
                By.XPATH,
                f"//div[contains(@class,'ant-select-item-option-content') and text()='{option_text}']"
            )
            js_click(driver, option)
            print(f"✅ '{option_text}' selected")
            found = True
            break
        except Exception:
            driver.execute_script("arguments[0].scrollTop += 200", dropdown)
            time.sleep(2)
    if not found:
        print(f"❌ '{option_text}' not found in dropdown")

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

# ══════════════════════════════════════════════════════════════════
#                        LAB BOOKING
# ══════════════════════════════════════════════════════════════════

def book_lab(driver, wait):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Add More Services') or contains(@class,'crm-outline-btn')]")
    )).click()
    print("✅ Add more services clicked")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Lab')]")
    )).click()
    print("✅ Lab clicked")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(., 'Hospital')]")
    )).click()
    print("✅ Lab @ Hospital selected")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-modal')]//div[contains(@class,'ant-select-single')]//div[@class='ant-select-selector']")
    )).click()
    print("Hospital dropdown is clicked successfully")
    time.sleep(3)

    hospital = wait.until(
    EC.presence_of_element_located(
        (By.XPATH,"//div[contains(@class,'ant-select-item-option') and @title='Medanta Hospital, Gurugram']")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",hospital)
    driver.execute_script("arguments[0].click();",hospital)
    print(f"✅ Hospital selected: {hospital.text}")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Continue')]")
    )).click()
    print("✅ Continue clicked")
    time.sleep(3)

    # All Bookings → New Booking → Search
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='All Bookings']")
    )).click()
    time.sleep(5)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='New Booking']")
    )).click()
    time.sleep(5)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
    )).click()
    print("✅ Search button is clicked successfully")
    time.sleep(3)

    # Add to cart
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[contains(text(),'Add To Cart')])[1]")
    )).click()
    print("✅ Lab test added to cart")
    time.sleep(5)

    # Go to cart
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='anticon']//*[name()='svg']")
    )).click()
    print("✅ Redirect to the cart page after clicking on cart button")
    time.sleep(5)

    # Add more lab
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-text text-primary p-0']")
    )).click()
    print("✅ Add More Lab button is clicked successfully")
    time.sleep(5)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[contains(text(),'Add To Cart')])[2]")
    )).click()
    print("✅ Additional lab test added to cart")
    time.sleep(10)

    # Go to cart again
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='anticon']//*[name()='svg']")
    )).click()
    print("✅ Redirect to the cart page after clicking on cart button")
    time.sleep(5)

    # Select slot
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-text']")
    )).click()
    print("✅ The select slot pop-up is opened successfully")
    time.sleep(5)

    select_first_available_slot(driver, wait)
    time.sleep(2)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
    )).click()
    print("✅ Lab slot confirmed")
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#                        EHC BOOKING
# ══════════════════════════════════════════════════════════════════

def book_ehc(driver, wait):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'Add More Services') or contains(@class,'crm-outline-btn')]")
    )).click()
    print("✅ Add more services clicked")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'EHC')]")
    )).click()
    print("✅ EHC clicked")
    time.sleep(3)

    # All Bookings → New Booking
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='All Bookings']")
    )).click()
    print("✅ Redirect to the All Bookings Page")
    time.sleep(5)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='New Booking']")
    )).click()
    print("✅ Redirect to the New Booking Page")
    time.sleep(5)

    # Region
    region_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[2]")
    ))
    region_dropdown.click()
    print("✅ Region dropdown is clicked successfully")
    time.sleep(3)

    region = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'ant-select-item-option')][1]")
    ))
    region.click()
    print(f"✅ Region selected : {region.text}")
    time.sleep(3)

    # Hospital
    hospital_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='ant-select-selector'])[3]")
    ))
    hospital_dropdown.click()
    print("✅ Hospital dropdown is clicked successfully")
    time.sleep(3)

    hospital = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(),'All Hospitals/Clinics')]")
    ))
    hospital.click()
    print(f"✅ Hospital selected : {hospital.text}")
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
        print("✅ Medanta Basic Health Check selected")
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

    # Search
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']")
    )).click()
    print("✅ Search button clicked")
    time.sleep(5)

    # Earliest
    earliest_availability = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Get Earliest Availability') and not(@disabled)]")
    ))
    earliest_availability.click()
    print(f"✅ Earliest availability clicked : {earliest_availability.text}")
    time.sleep(5)

    # Select Slot
    slot = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//button[contains(., 'Select Slot')])[1]")
    ))
    slot.click()
    print(f"✅ Select slot button clicked")
    time.sleep(7)

    select_first_available_slot(driver, wait)
    time.sleep(2)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-col ant-col-10']//button[@type='button']")
    )).click()
    print("✅ EHC added to cart")
    time.sleep(3)

    # Book Now → Confirm
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Book Now']")
    )).click()
    print("✅ Book Now button clicked")
    time.sleep(3)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Confirm Booking']")
    )).click()
    print("✅ Confirm Booking button clicked")
    time.sleep(5)

    close_modal(wait)
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#                 CREATE PATIENT ADDRESS
# ══════════════════════════════════════════════════════════════════

def fill_patient_address(wait, address1, address2, pincode):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='complex-form_address_line_1']")
    )).send_keys(address1)
    print(f"✅ Address line 1 : {address1}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='complex-form_address_line_2']")
    )).send_keys(address2)
    print(f"✅ Address line 2 : {address2}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='complex-form_pincode']")
    )).send_keys(pincode)
    print(f"✅ Pincode : {pincode}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Create Patient']")
    )).click()
    print("✅ Patient created")
    time.sleep(20)

# ══════════════════════════════════════════════════════════════════
#                 CREATE CONTACT
# ══════════════════════════════════════════════════════════════════

def create_new_contact(driver, wait, title, first, last, dob_year, dob_month, dob_day, gender, email):
    create_new_contact_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-lg ant-btn-block']")
    ))
    create_new_contact_button.click()
    print("Add new contact clicked")
    time.sleep(2)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='createContactForm_salutation']")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(@class,'ant-select-item-option-content') and text()='{title}']")
    )).click()
    print(f"Title set: {title}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='createContactForm_first_name']")
    )).send_keys(first)
    print(f"First name set: {first}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='createContactForm_last_name']")
    )).send_keys(last)
    print(f"Last name set: {last}")
    time.sleep(1)

    # Date of Birth
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@placeholder='Select date']")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-picker-header-view')]")
    )).click()

    while True:
        header = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'ant-picker-header-view')]")
        )).text
        decade_start = (dob_year // 10) * 10
        if str(decade_start) in header:
            break
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'ant-picker-header-super-prev-btn')]")
        )).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//td//div[text()='{dob_year}']")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//td//div[text()='{dob_month}']")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//td//div[text()='{dob_day}']")
    )).click()
    print(f"DOB set: {dob_year}-{dob_month}-{dob_day}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='createContactForm_gender_id']")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(@class,'ant-select-item-option-content') and text()='{gender}']")
    )).click()
    print(f"Gender set: {gender}")
    time.sleep(1)

    email_field = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='createContactForm_email']")
    ))
    email_field.send_keys(email)
    print(f"Email set: {email}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Create Contact']")
    )).click()
    print("✅ Contact created")
    time.sleep(3)

    patient_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='ant-select-selector']//div[1]")
    ))
    time.sleep(2)
    patient_dropdown.click()
    print("✅ Patient dropdown open")
    time.sleep(3)

    first_patient = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[contains(@class,'ant-select-item-option')])[1]")
    ))
    first_patient.click()
    print("✅ Patient selected")
    time.sleep(3)

# ══════════════════════════════════════════════════════════════════
#                 CALL LOG SECTION
# ══════════════════════════════════════════════════════════════════

def handle_call_log(driver, wait, default_uhid="MM02929789", default_phone="2112000000"):
    call_logs = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@title='Call Log']//*[name()='svg']")
    ))
    call_logs.click()
    print("Call Log tab opened")
    time.sleep(5)

    clear_date_filter(
        driver, wait,
        "//input[@id='generic_filters_range']",
        "//span[@class='ant-picker-clear']"
    )
    # Search by phone
    search_field = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='generic_filters_phone']")
    ))
    search_field.send_keys("7011209294")
    time.sleep(5)

    first_call_log = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//tr[contains(@class,'ant-table-row')]//td[1]//a)[1]")
    ))
    first_call_log.click()
    print("First call log opened")
    time.sleep(3)

    # UHID Search
    uhid_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='uhid']")
    ))
    uhid_field.click()
    uhid_field.send_keys(Keys.CONTROL + "a")
    uhid_field.send_keys(Keys.DELETE)
    print("Waiting 10 seconds for UHID entry...")
    time.sleep(10)

    current = uhid_field.get_attribute('value')
    if not current:
        uhid_field.send_keys(default_uhid)
        print(f"Default UHID entered: {default_uhid}")
    else:
        print(f"UHID detected: {current}")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[@aria-label='search'])[2]")
    )).click()
    time.sleep(5)

    try:
        error = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, 'ant-message') or contains(text(), 'not found')]")
        ))
        print(f"❌ Error: {error.text}")
    except TimeoutException:
        print("🎉 Data loaded successfully for UHID")

    # Phone Number Search
    phone_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='phoneNumber']")
    ))
    phone_field.send_keys(Keys.CONTROL + "a")
    phone_field.send_keys(Keys.DELETE)
    print("Waiting 10 seconds for phone number entry...")
    time.sleep(10)

    current = phone_field.get_attribute('value')
    if not current:
        phone_field.send_keys(default_phone)
        print(f"Default phone entered: {default_phone}")
    else:
        print(f"Phone detected: {current}")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[@aria-label='search'])[1]")
    )).click()
    time.sleep(5)

    # Advanced Search
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//u[normalize-space()='Advanced Search']")
    )).click()
    time.sleep(5)

    first_name_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='first_name']")
    ))
    first_name_field.send_keys("Rahul")
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Search']")
    )).click()
    time.sleep(5)

    result = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(text(),'Found')]")
    ))
    print(result.text)
    time.sleep(3)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='close']")
    )).click()
    print("Advanced Search closed")
    time.sleep(2)

#=========================================================================================
#                OPD CONSULTATION/EHC/RADIOLOGY APPOINTMENT COUNTS
#=========================================================================================
def select_all_speciality_and_doctors(wait):
    opd = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='OPD']//*[name()='svg']")))
    opd.click()
    print("✅User clicked on the OPD tab")
    time.sleep(2)
 
    remove_speciality = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@title='Internal Medicine']//span[@aria-label='close']//*[name()='svg']"))
    )
    remove_speciality.click()
    print("✅User remove the speciality filter")
    time.sleep(2)
 
    speciality = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[4]")))
    speciality.click()
    print("✅ Speciality dropdown is clicked successfully")
    time.sleep(3)
 
    search_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'ant-select-selection-overflow')])[1]//input"))
    )
    search_input.send_keys("All Speciality")
    time.sleep(1)
 
    try:
        option = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class,'ant-select-item-option-content') and contains(text(),'All') and contains(text(),'Speciality')]"
        )))
        #driver = option._parent  # noqa
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", option)
        print("✅ All Speciality selected")
    except Exception:
        print("⚠️ Direct click failed/timed out. Attempting Keyboard Navigation fallback...")
        search_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.3)
        search_input.send_keys(Keys.ENTER)
        print("✅ All Speciality selected via Keyboard Enter")
 
    doctor_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[5]")))
    doctor_field.click()
    print("✅ Doctor dropdown clicked")
    time.sleep(2)
 
    search_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-selection-overflow'])[2]//input"))
    )
    search_input.send_keys("All Doctors")
    print("🔍 Searching for All Doctors")
    time.sleep(2)
 
    option_xpath = (
        "//div[contains(@class,'ant-select-item-option')]"
        "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='All Doctors']"
    )
    try:
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", option)
        print("✅ All Doctors selected")
    except Exception:
        print("⚠️ All Doctors option not clickable. Trying keyboard navigation...")
        search_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(@class,'ant-select-selection-overflow')])[2]//input"))
        )
        search_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        print("✅ All Doctors selected via Keyboard Enter")
 
    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Search']")))
    search.click()
    print("✅ Search button clicked : All Appointments are visible")
    time.sleep(5)
 
 
def read_appointment_tab_counts(wait, tabs):
    """
    tabs: dict of {data-node-key: display label}
    Clicks each tab and prints its count parsed from the tab text.
    """
    for key, tab_name in tabs.items():
        try:
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-node-key='{key}']//div[@role='tab']")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
            tab.click()
            time.sleep(2)
 
            tab_text = tab.text.strip()
            count_str = tab_text.split(":")[-1].strip()
            count = int(count_str) if count_str.isdigit() else 0
            print(f"✅ {tab_name} : {count}")
        except Exception:
            print(f"❌ {tab_name} : Unable to get count")
 
 
def check_opd_appointment_counts(wait):
    tabs = {
        "all": "All Appts.",
        "check-in": "Check-In",
        "check-out": "Check-Out",
        "cancelled": "Cancel",
        "not-cancelled": "Confirmed",
        "queue": "Queue",
    }
    read_appointment_tab_counts(wait, tabs)
 
 
def check_ehc_appointment_counts(driver, wait):
    service = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]")))
    service.click()
    print("✅ Service dropdown clicked")
    time.sleep(1)
    _select_dropdown_option(driver, wait, "EHC")
 
    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Search']")))
    search.click()
    print("✅ Search button clicked : All Appointments are visible")
    time.sleep(5)
 
    tabs = {"all": "All Appts.", "cancelled": "Cancel", "not-cancelled": "Confirmed"}
    read_appointment_tab_counts(wait, tabs)
 
 
def check_radiology_appointment_counts(driver, wait):
    service = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]")))
    service.click()
    print("✅ Service dropdown clicked")
    time.sleep(1)
    _select_dropdown_option(driver, wait, "Radiology")
 
    machine = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[5]")))
    machine.click()
    print("✅ Machine dropdown clicked")
    time.sleep(2)
    _select_dropdown_option(driver, wait, "All Machine")
 
    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Search']")))
    search.click()
    print("✅ Search button clicked : All Appointments are visible")
    time.sleep(5)
 
    tabs = {"all": "All Appts.", "cancelled": "Cancel", "not-cancelled": "Confirmed"}
    read_appointment_tab_counts(wait, tabs)
 
# ══════════════════════════════════════════════════════════════════
#                 CREATE LEAD
# ══════════════════════════════════════════════════════════════════

def create_lead(wait, phone="3469000000"):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Create Lead']")
    )).click()
    print("Create Lead clicked")
    time.sleep(3)

    phone_field = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='phone_number']")
    ))
    phone_field.send_keys(phone)
    print(f"Phone entered: {phone}")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[@aria-label='search'])[1]")
    )).click()
    time.sleep(5)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='selectedPatient']")
    )).click()
    time.sleep(2)

    selected_patient = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'ant-select-item-option-content')][1]")
    ))
    selected_patient.click()
    print(f"✅ First patient selected for new lead:{selected_patient}")
    time.sleep(2)

# ══════════════════════════════════════════════════════════════════
#                    PAYMENT LINK FLOW
# ══════════════════════════════════════════════════════════════════

def handle_payment_link_flow(driver, wait):
    lead_tab = driver.current_window_handle

    click_tab(wait, "Communication History")

    view_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(@class,'ant-typography')][normalize-space()='View Message'])[1]")
    ))
    view_message.click()
    print("View Message opened")
    time.sleep(2)

    payment_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'medantabeta') or contains(text(),'http://medantabeta')]")
    ))
    payment_link.click()
    print(f"Payment link clicked: {payment_link.text}")
    print("Waiting 60 seconds for payment to complete...")
    time.sleep(60)  # was 90 — adjust back up if real manual payment needs more time

    # Switch back to Lead tab
    driver.switch_to.window(lead_tab)
    print("✅ Switched back From Payment tab to CRM tab")

    close_modal(wait)
    time.sleep(1)

    back_to_leaddetails = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@title='Leads']//*[name()='svg']")
    ))
    back_to_leaddetails.click()
    print("Back to Lead Details tab")
    time.sleep(1)  # was 2

# ══════════════════════════════════════════════════════════════════
#                    PATIENT 360
# ══════════════════════════════════════════════════════════════════

def go_to_patient_360(wait):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='more']")
    )).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@class='ant-dropdown-menu-item']")
    )).click()
    print("✅ Navigated to Patient 360")
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#                        MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════

def main():
    try:
        #-----1. Login-------------------------
        login(driver, wait,
            url="https://betamedi-crmui.medanta.org:5443/medanta/crm/login",
            mobile="7011209294",
            otp_digits=["3", "2", "1", "5", "6", "4"]
        )
        time.sleep(25)

        #-----2. Ticket Tab----------
        clear_date_filter(driver, wait,
            "//input[@id='moreFilters_range']",
            "//span[@aria-label='close-circle']"
        )
        rows = get_table_rows(driver, wait)
        if open_first_row(driver, rows, label="ticket"):
            handle_ticket_detail_flow(driver, wait, detail_tab_text="Ticket Details")

    #-----3. More Filters----------
        apply_more_filters(driver, wait)

    #-----4. Download Report----------
        download_ticket_report(driver, wait, email="rsingh@medanta.org")

    # ── Ticket : Process each ticket status tab ──
        for status in ["Closed"]:
            process_status_tab(driver, wait, tab_span_text=status,
                            item_label="ticket", detail_tab_text="Ticket Details")

    #-----5. Leads Tab----------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@title='Leads']//*[name()='svg']")
        )).click()
        print("Leads tab opened")
        time.sleep(5)

        clear_date_filter(driver, wait,
            "//input[@id='moreFilters_range']",
            "//span[@class='ant-picker-clear']"
        )

        rows = get_table_rows(driver, wait)
        if open_first_row(driver, rows, label="lead"):
            handle_ticket_detail_flow(driver, wait, detail_tab_text="Lead Details")

    # ── Lead : Process each lead status tab ──
        for status in ["Follow-up"]: 
            process_status_tab(driver, wait, tab_span_text=status,
                            item_label="lead", detail_tab_text="Lead Details")

    # ── Back to New leads, open 1st, book services ──
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='New']")
        )).click()
        time.sleep(5)

        search_bar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='moreFilters_search_val']")
        ))
        search_bar.send_keys("7011209294")
        time.sleep(5)

        rows = get_table_rows(driver, wait)
        if open_first_row(driver, rows, label="lead"):
            book_consult_appointment(driver, wait)
            edit_consult_slot(driver, wait)
            book_radiology(driver, wait)
            book_lab(driver, wait)
            book_ehc(driver, wait)
            handle_payment_link_flow(driver, wait)
 
    #------6. OPD Section------------
        select_all_speciality_and_doctors(wait)
        check_opd_appointment_counts(wait)
        check_ehc_appointment_counts(driver, wait)
        check_radiology_appointment_counts(driver, wait)
        

    #-----7. Call Log----------
        handle_call_log(driver, wait)

    #-----8. Create Contact----------
        create_new_contact(driver, wait,
            title="Mr.", first="Rajan", last="Kumar",
            dob_year=1997, dob_month="Mar", dob_day=29,
            gender="male", email="rohit.sharma@thb.co.in"
        )

        go_to_patient_360(wait)

    # ── Book Consult (with specific doctor), Radiology, Lab, EHC ──
        book_consult_appointment(driver, wait)

        fill_patient_address(wait,
            address1="Paras Society,Sector 105",
            address2="Gurugram,Haryana",
            #state_text="Haryana",
            #city_text="Gurugram",
            pincode="122001"
        )
        book_radiology(driver, wait)
        book_lab(driver, wait)
        book_ehc(driver, wait)

    # ── Patient 360 → Communication → Payment ──
        handle_communication_history(driver, wait)
        handle_payment_link_flow(driver, wait)

    # ── Create Lead ──
        '''create_lead(wait, phone="4140000000")'''

        print("\n\n✅✅✅  ALL FLOWS COMPLETED SUCCESSFULLY  ✅✅✅")
    
    except KeyboardInterrupt:
        print("\n⏹️ Script interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR in main flow: {e}")
        driver.save_screenshot("critical_error.png")

    finally:
        time.sleep(30)
        save_output_to_pdf()
        driver.quit()
        print("🔒 Browser closed")


if __name__ == "__main__":
    main()
