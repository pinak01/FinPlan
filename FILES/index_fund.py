from playwright.sync_api import sync_playwright

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.etmoney.com/mutual-funds/featured/best-index-funds/12")

        page.wait_for_selector('.scheme-name')  # Assuming the fund name has this class, adjust as needed
        page.wait_for_selector('.current-value')
        # Scrape the data
        fund_names = page.query_selector_all('.scheme-name')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.current-value')
        
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        
        i=0
        # Print or return the scraped data
        for idx, fund in enumerate(fund_list, 1):
            print(f"{idx}. {fund}")
            print(f"Current Value: {details1[i]}")
            print("\n")
            i=i+1
        browser.close()

scrape_ultra_short_funds()