from playwright.sync_api import sync_playwright
import json

cyclicalstocks = []

def scrape_ultra_short_funds():
    with sync_playwright() as p:
        global cyclicalstocks
        browser = None
        try:
            # Launch the browser
            browser = p.chromium.launch(headless=False)  # Set headless=False if you want to see the browser
            page = browser.new_page()

            # Navigate to the Screener page
            page.goto("https://www.etmoney.com/stocks/market-data/high-dividend-yield-stocks/36")

            # Scrape the data
            fund_names = page.query_selector_all('table tbody tr')  # Adjust the selector based on the fund name's CSS class
            details = fund_names
            j=0
            for i in details:
                    try:
                        # Extract the data for each row
                        fund_data = i.query_selector_all('td')
                        data = {
                            "Company": fund_data[0].text_content(),  # Uncomment this if needed
                            "LTP": fund_data[1].text_content(),
                            "Return": fund_data[2].text_content(),
                            "Market Cap": fund_data[3].text_content(),
                            "High/Low": fund_data[4].text_content(),
                            "Dividend Yeild": fund_data[5].text_content(),
                        }
                        cyclicalstocks.append(data)


                    except Exception as row_error:
                        print(f"Error processing row {j}: {row_error}")
                        continue  # Skip to the next row if an error occurs

            # Print the collected data
            print(json.dumps(cyclicalstocks, indent=2))

        except Exception as browser_error:
            print(f"An error occurred while scraping: {browser_error}")

        finally:
            if browser:
                browser.close()  # Ensure the browser closes even if an error occurs

# Run the scraper
scrape_ultra_short_funds()
