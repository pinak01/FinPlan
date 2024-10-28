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
            page.goto("https://www.screener.in/screens/1074720/cyclical-stocks/")

            # Scrape the data
            fund_names = page.query_selector_all('table.data-table.text-nowrap.striped.mark-visited tbody tr')  # Adjust the selector based on the fund name's CSS class
            details = fund_names[1:]
            j = 0
            for i in details:
                if j < 15:
                    try:
                        # Extract the data for each row
                        fund_data = i.query_selector_all('td')
                        data = {
                            "Fund Name": fund_data[1].text_content(),  # Uncomment this if needed
                            "Current Price": fund_data[2].text_content(),
                            "Price to Earning": fund_data[3].text_content(),
                            "Market Cap": fund_data[4].text_content(),
                            "Dividend Yield": fund_data[5].text_content(),
                            "Net Profit": fund_data[6].text_content(),
                            "Profit Growth": fund_data[7].text_content(),
                            "Sales": fund_data[8].text_content(),
                            "Sales Qtr": fund_data[9].text_content(),
                            "ROCE": fund_data[10].text_content(),
                            "Profit Var": fund_data[11].text_content(),
                            "ROE": fund_data[12].text_content(),
                            "Sales": fund_data[13].text_content(),
                        }
                        cyclicalstocks.append(data)
                        j += 1  # Increment the counter

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
