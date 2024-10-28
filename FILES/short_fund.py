from playwright.sync_api import sync_playwright
import json

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/mutual-funds/category/best-ultra-short-mutual-funds")

        # Wait for the content to load
        page.wait_for_selector('.stfs4Anchor')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.stfs4Anchor')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        funds_json = []
        i = 0
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "category": details1[68 + i],
                "Risk": details1[69 + i],
                "1 yr Return": details1[70 + i],
                "Fund Size in Cr": details1[72 + i][1:]
            }
            funds_json.append(fund_data)
            i += 6

        # Convert to JSON
        json_output = json.dumps(funds_json, indent=1)

        # Print the JSON data
        print(json_output)


        # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
