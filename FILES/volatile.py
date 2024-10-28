from playwright.sync_api import sync_playwright
import json 
def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://in.tradingview.com/markets/stocks-india/market-movers-most-volatile/")

        # Wait for the content to load
        page.wait_for_selector('.apply-common-tooltip')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.tickerDescription-GrtoTeat')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.cell-RLhfr_y4.right-RLhfr_y4')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        i = 0
        fund_data = []  # List to hold the funds data

        # Iterate through the fund list and capture details
        for idx, fund in enumerate(fund_list, 1):
            fund_details = {
                "Fund": fund,
                "Detail 1": details1[i],
                "Detail 2": details1[i+1],
                "Detail 3": details1[i+2],
                "Detail 4": details1[i+3],
                "Detail 5": details1[i+4],
                "Detail 6": details1[i+5],
                "Detail 7": details1[i+6][1:],
                "Detail 8": details1[i+7][1:],
                "Detail 9": details1[i+8][1:],
                "Detail 10": details1[i+9]
            }
            fund_data.append(fund_details)
            i += 10

        # Convert the list to JSON format
        fund_json = json.dumps(fund_data, indent=4)

        # Output the JSON data (or save to a file if needed)
        print(fund_json)

                # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
