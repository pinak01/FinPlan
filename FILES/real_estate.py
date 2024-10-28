from playwright.sync_api import sync_playwright
import json

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/stocks/sectors/real-estate")

        # Wait for the content to load
        page.wait_for_selector('.st76SymbolName')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.st76SymbolName')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.st76DivSec')
        close=page.query_selector_all('.st76Pad16')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        close1=[close1.inner_text() for close1 in close]
        i = 0
        j=1
        funds_json = []

        # Build the data structure for JSON
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "close": close1[i][1:],
                "market Cap in cr": close1[j][1:]
            }
            funds_json.append(fund_data)
            i += 2
            j=j+2
        # Convert to JSON
        json_output = json.dumps(funds_json, indent=4)

        # Print the JSON data
        print(json_output)

        # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
