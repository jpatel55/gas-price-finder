from fpdf import FPDF
from fpdf.enums import XPos, YPos
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Configure Selenium WebDriver options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--ignore-certificate-errors")
options.add_argument("--log-level=3")

# List of valid US state abbreviations
valid_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Prompt user for search criteria
print("Search gas stations by:")
print("1. City, State")
print("2. ZIP code")
user_choice = input("Enter your choice (1 or 2): ")
print()

flag = True  # Validation flag

# Handle user input and validate
if user_choice == "1":
    city = input("Enter city: ").title()
    state = input("Enter state (two-letter): ").upper()
    if state not in valid_states:
        print("Invalid state")
        flag = False
elif user_choice == "2":
    zipcode = input("Enter 5-digit ZIP code: ")
    if len(zipcode) != 5 or not zipcode.isdigit():
        print("Invalid ZIP code")
        flag = False
else:
    print("Invalid choice")
    flag = False

if flag:
    data = []  # Store extracted gas station details
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://cluballiance.aaa.com/public-affairs/gas-information")
    wait = WebDriverWait(driver, 10)

    # Locate the ZIP code input field
    zip_code_field = wait.until(EC.element_to_be_clickable((By.NAME, 'zipCode')))
    zip_code_field.clear()

    # Fill in search fields based on user choice
    if user_choice == "1":
        city_field = wait.until(EC.element_to_be_clickable((By.NAME, 'city')))
        city_field.send_keys(city)
        state_dropdown = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
        select = Select(state_dropdown)
        select.select_by_visible_text(state)
    elif user_choice == "2":
        zip_code_field.send_keys(zipcode)
    
    # Click the "Find gas" button
    find_gas_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Find gas']")))
    find_gas_button.click()
    
    try:
        # Check if an error message appears (no data found case)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_aaaSearch_SearchError"))
        )
        print("No data found")
    except:
        # Extract gas station data if available
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_searchResults_stationList_gvResults")))
        gas_station_rows = driver.find_elements(By.CSS_SELECTOR, "tr.ResultGridViewItem, tr.ResultGridViewAlternatingItem")
        
        print("\n" + "=" * 80)
        print(f"{'STATION':<28}{'ADDRESS':<45}{'REG GAS':<7}")
        print("=" * 80)

        count = 0  # Track number of results
        for row in gas_station_rows:
            try:
                gas_station_name = row.find_element(By.XPATH, ".//td/table/tbody/tr[1]/td/a").text.strip()
                address_first_line = row.find_element(By.XPATH, ".//td[2]/table/tbody/tr[1]/td/a").text.strip()
                address_second_line = row.find_element(By.XPATH, ".//td[2]/table/tbody/tr[2]/td").text.strip()
                full_address = f"{address_first_line}, {address_second_line}"
                maps_url = f"https://www.google.com/maps/search/?api=1&query={quote_plus(full_address)}"
                price = row.find_element(By.XPATH, ".//td[3]/table/tbody/tr[1]/td/span").text.strip()
                
                count += 1
                print(f"{gas_station_name:<28}{full_address:<45}{price:<7}")
                
                data.append({
                    "name": gas_station_name,
                    "address": full_address,
                    "price": price,
                    "link": maps_url
                })
                
                if count == 10:  # Limit to top 10 results
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
    
    driver.quit()

    # Generate a PDF report with a concise name including the date
    report_name = f"Gas_Stations_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=8)
    pdf.cell(200, 10, text="Top 10 Gas Stations", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    for station in data:
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Helvetica", style='U', size=8)
        x, y = pdf.get_x(), pdf.get_y()
        pdf.cell(0, 10, text=station["name"], new_x=XPos.RIGHT, new_y=YPos.TOP, link=station["link"])
        pdf.set_xy(x + 35, y)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", size=8)
        pdf.cell(0, 10, text=station['address'], new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_xy(x + 100, y)
        pdf.cell(0, 10, text=station['price'], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    pdf.output(report_name)
