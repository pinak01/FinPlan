from playwright.sync_api import sync_playwright

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.screener.in/screens/421894/preferred-stocks")

        # Wait for the content to load
        page.wait_for_selector('.text')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.text')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('td')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        i=2;
        # Print or return the scraped data
        for  fund in enumerate(fund_list):
            print(f"{fund}")
            print(f"Details: {details1[i]}")
            print("\n")
            i=i+13

        # Close the browser
        browser.close()

# Run the scraper
scrape_ultra_short_funds()
