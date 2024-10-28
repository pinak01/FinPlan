from playwright.sync_api import sync_playwright
import json

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.wintwealth.com/bonds/corporate-bonds")

        # Wait for the content to load
        page.wait_for_selector('.sc-5db653c-7')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.sc-5db653c-7')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.row-description')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        funds_json = []
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "Issue_size": details1[i],
                "Maturity":details1[i+1],
            }
            funds_json.append(fund_data)
            i += 4

        # Convert to JSON
        json_output = json.dumps(funds_json, indent=1)

        # Print the JSON data
        print(json_output)


        # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
