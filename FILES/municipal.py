from playwright.sync_api import sync_playwright
import json

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.sebi.gov.in/statistics/municipalbonds.html")

        # Wait for the content to load
        page.wait_for_selector('.org-table-1')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('td')  # Adjust the selector based on the fund name's CSS class
        #details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        #details1=  [detail.inner_text() for detail in details]
        funds_json = []
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund_list[i],
                "Date_of_issue":fund_list[i+1],
                "Date_of_maturity":fund_list[i+2],
                "Amount_in_Cr":fund_list[i+3],
                "Tenure_in_yrs":fund_list[i+5]
            }
            i=i+8
            if (idx==10):
                break
            funds_json.append(fund_data)
            

        # Convert to JSON
        json_output = json.dumps(funds_json, indent=1)

        # Print the JSON data
        print(json_output)


        # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
