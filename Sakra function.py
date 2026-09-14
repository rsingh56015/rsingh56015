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

# ══════════════════════════════════════════════════════════════════
#                        BROWSER SETUP
# ══════════════════════════════════════════════════════════════════
def setup_driver():
    options = Options()
    options.add_argument("--force-device-scale-factor=0.80")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='80%'")
    return driver

driver = setup_driver()
wait = WebDriverWait(driver, 30)

# ══════════════════════════════════════════════════════════════════
#                        LOGIN
# ══════════════════════════════════════════════════════════════════

def login(driver, wait, url, username, password):
    driver.get(url)
    print(driver.title)

    username_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='email']")
    ))
    username_input.send_keys(username)
    print(f"Username entered: {username}")

    password_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='password']")
    ))
    password_input.send_keys(password)
    print(f"Password entered: {password}")

    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Sign in']")
    ))
    submit_btn.click()
    print("Login successful")
    time.sleep(15)

# ══════════════════════════════════════════════════════════════════
#                     COMMON HELPERS
# ══════════════════════════════════════════════════════════════════
# After login, the user 1st redirected to the Admin module, then the user clicks on Admin to open the option of Sakra Operation CRM

def click_sakra_status_tab(driver, wait):
    """Click a status tab (All, New, Valid, Follow Up, Converted, Denied, Invalid) in Sakra CRM."""
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//table | //div[@role='table']")))
    rows = driver.find_elements(By.XPATH, "//tbody/tr")  # adjust selector to match actual row container
    print(f"Rows found on this page: {len(rows)}")
    return rows

def get_table_rows(driver, wait):
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//tbody[contains(@class,'ant-table-tbody')]")
    ))
    rows = driver.find_elements(
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]/tr[not(@aria-hidden='true')]"
    )
    print(f"Rows found: {len(rows)}")
    return rows

def open_first_row(driver, rows, label="ticket"):
    if len(rows) == 0:
        print(f"⚠️ No {label}s available")
        return False
    first_item = rows[0].find_element(By.XPATH, ".//a[contains(@class,'bold-600')]")
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
    print(f"Navigated to '{tab_text}' tab")
    time.sleep(3)

def go_back_to_list(wait):
    back_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@aria-label='arrow-left']//*[name()='svg']")
    ))
    back_btn.click()
    print("Navigated back to list page")
    time.sleep(5)

def close_modal(wait):
    close_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@aria-label='Close']")
    ))
    close_btn.click()
    print("Modal closed")
    time.sleep(2)

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

# ══════════════════════════════════════════════════════════════════
#              FULL TICKET/LEAD DETAIL FLOW
# ══════════════════════════════════════════════════════════════════

def handle_lead_detail_flow(driver, wait, detail_tab_text="Details"):
    click_tab(wait, "Activity History")
    time.sleep(5)

    click_tab(wait, detail_tab_text)
    time.sleep(5)

    go_back_to_list(wait)

# ══════════════════════════════════════════════════════════════════
#            TICKET : NAVIGATE TO STATUS TAB AND PROCESS FIRST ITEM
# ══════════════════════════════════════════════════════════════════

def process_status_tab(driver, wait, tab_span_text, item_label="leads", detail_tab_text="Details"):
    tab = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[normalize-space()='{tab_span_text}']")
    ))
    tab.click()
    print(f"Navigated to '{tab_span_text}' tab")
    time.sleep(5)

    rows = get_table_rows(driver, wait)

    if not open_first_row(driver, rows, label=item_label):
        return

    handle_lead_detail_flow(driver, wait, detail_tab_text=detail_tab_text)
    print(f"✅ '{tab_span_text}' tab flow complete")

# ══════════════════════════════════════════════════════════════════
#                    MORE FILTERS
# ══════════════════════════════════════════════════════════════════

def apply_more_filters(driver, wait):
    more_filter = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='More Filters']")
    ))
    more_filter.click()
    print("More Filters opened")
    time.sleep(2)

    filter_xpaths = {
        "Assignee": "(//span[contains(text(),'Select multiple...')])[1]",
        "Hospital": "(//span[contains(text(),'Select multiple...')])[2]",
        "Event": "(//span[contains(text(),'Select multiple...')])[3]",
        "Opportunities": "(//span[contains(text(),'Select multiple...')])[4]",
        "Priority": "(//span[contains(text(),'Select multiple...')])[5]",
        "Source": "(//span[contains(text(),'Select multiple...')])[6]"
    }

    # -----------------------------
    # Select Source = Call Logs
    # -----------------------------

    # Click Source dropdown
    source_filter = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, filter_xpaths["Source"])
        )
    )
    driver.execute_script("arguments[0].click();", source_filter)

    # Select "Call Logs"
    call_logs_option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//span[contains(text(),'Call Logs')])[2]")
        )
    )
    driver.execute_script("arguments[0].click();", call_logs_option)

    # -----------------------------
    # Click Apply
    # -----------------------------

    apply_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Apply']")
        )
    )
    driver.execute_script("arguments[0].click();", apply_button)

    print("Source filter 'Call Logs' selected and applied successfully.")

    for name, xpath in filter_xpaths.items():
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            field.click()
            print(f"'{name}' filter clicked — any selection or blank is acceptable")
        except Exception as e:
            print(f"⚠️ Could not click '{name}' filter: {e}")
        time.sleep(2)

    more_filter_close = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='More Filters']")
    ))
    js_click(driver, more_filter_close)
    print("More Filters closed")
    time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#                        MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════

def main():
    try:
        #-----1. Login-------------------------
        login(driver, wait,
            url="https://metacrm.k8s-dev.hlthclub.in/login?tenant=sakra&returnUrl=%2Fsakra%2Fapp%2Fsakra%2Fpage%2Fsakra-operations",
            username="admin@dev.com",
            password="Cu*ost93A#r&"
        )
        time.sleep(3)

        leads = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,"//span[normalize-space()='Leads']")
            )
        )
        #driver.execute_script("arguments[0].click();", leads)
        leads.click()
        print("Leads tab clicked")
        time.sleep(5)

        all_leads = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html[1]/body[1]/div[2]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/button[3]")
            )
        )
        all_leads.click()
        print("All Leads tab clicked")
        time.sleep(2)

        click_sakra_status_tab(driver, wait)

        rows = get_table_rows(driver, wait)
        if open_first_row(driver, rows, label="Leads"):
            handle_lead_detail_flow(driver, wait, detail_tab_text="Details")

    #-----3. More Filters----------
        apply_more_filters(driver, wait)

    # ── Leads : Process each ticket status tab ──
        for status in ["New", "Valid", "Follow-up", "Converted", "Denied", "Invalid"]:
            process_status_tab(driver, wait, tab_span_text=status,
                            item_label="leads", detail_tab_text="Details")

    #-----5. Leads Tab----------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@title='Leads']//*[name()='svg']")
        )).click()
        print("Leads tab opened")
        time.sleep(5)

        search_bar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='moreFilters_search_val']")
        ))
        search_bar.send_keys("3210000000")
        time.sleep(8)

        rows = get_table_rows(driver, wait)
        if open_first_row(driver, rows, label="lead"):
            handle_lead_detail_flow(driver, wait, detail_tab_text="Lead Details")

    # ── Lead : Process each lead status tab ──
        for status in ["Follow-up","Converted","Denied","Closed"]: 
            process_status_tab(driver, wait, tab_span_text=status,
                            item_label="lead", detail_tab_text="Lead Details")

    # ── Back to New leads, open 1st, book services ──
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='New']")
        )).click()
        time.sleep(5)

        rows = get_table_rows(driver, wait)

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='selectedPatient']")
        )).click()
        time.sleep(3)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[contains(@class,'ant-select-item-option')])[1]")
        )).click()
        time.sleep(3)


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