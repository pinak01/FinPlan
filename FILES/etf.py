import asyncio
from playwright.async_api import async_playwright
import json

final_etf=[]
async def run(playwright):
    # Launch the browser
    global final_etf
    browser = await playwright.chromium.launch(headless=False)  # Set headless=True to run in the background
    page = await browser.new_page()

    # Navigate to the page with the ETF table (replace with the actual URL)
    await page.goto('https://groww.in/etfs')  # Replace with the actual URL

    # Wait for the table to load
    await page.wait_for_selector('table.tb10Table')

    # Extract data from each row of the ETF table
    etf_data = await page.evaluate('''() => {
        const rows = document.querySelectorAll('table.tb10Table tbody tr');
        return Array.from(rows).map(row => {
            const cells = row.querySelectorAll('td');
            return {
                etf_name: cells[0]?.innerText.trim(),
                market_price: cells[2]?.innerText.trim(),
                low_52_week: cells[3]?.innerText.trim(),
                high_52_week: cells[4]?.innerText.trim(),
            };
        });
    }''')

    # Print extracted ETF data
    # for etf in etf_data:
    #     # print(etf)
    #     data = {
    #             "Etf-Name": etf.etf_name,
    #             "Market-Price": etf.market_price,
    #             "Percentage-Change": etf.percentage_change,
    #             "Low":etf.low_52_week,
    #             "High":etf.high_52_week,
    #         }
    #     etf_data.append(data)
    obj = json.dumps(etf_data, indent=1)
    print(obj)
    # Close the browser
    await browser.close()

# Main function to run Playwright
async def main():
    async with async_playwright() as playwright:
        await run(playwright)

# Run the async main function
asyncio.run(main())