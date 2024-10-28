import asyncio
import json
import requests
from playwright.async_api import async_playwright

async def access_table():
    final = []  # List to store row data as objects

    async with async_playwright() as p:
        # Launch Firefox browser instead of Chromium
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        # Add headers to mimic a real browser
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        # Navigate to the page containing the table
        await page.goto('https://www.nseindia.com/report-detail/display-bulk-and-block-deals')

        # Wait for the table to load by waiting for the network to be idle
        await page.wait_for_load_state('networkidle')

        # You may need to wait a bit more for JavaScript to fully load the table
        await asyncio.sleep(10)

        # Wait for the table to appear
        await page.wait_for_selector('#HistBulkBlockDataTable', timeout=60000)

        # Select the table
        table = await page.query_selector('#HistBulkBlockDataTable')

        # If the table is not found, log an error
        if not table:
            print("Table not found")
            await browser.close()
            return

        # Get all rows of the table
        rows = await table.query_selector_all('tr')

        # Debugging: Log how many rows were found
        print(f"Found {len(rows)} rows.")

        # Define the keys for the table data
        keys = ["Date", "Symbol", "SrName", "CliName", "Work", "Quan", "Price", "Dash"]

        # Loop through each row
        for row in rows:
            cells = await row.query_selector_all('td')

            if len(cells) == len(keys):  # Make sure row has the correct number of cells
                obj = {}
                for i, cell in enumerate(cells):
                    cell_text = await cell.text_content()
                    obj[keys[i]] = cell_text.strip()  # Assign cell content to the corresponding key
                final.append(obj)
            else:
                print(f"Skipping row with {len(cells)} cells (expected {len(keys)}).")

        # Close the browser
        await browser.close()

        # If final array is empty, log an error
        if not final:
            print("No data found in the table.")
            return

        # Convert final array to JSON
        json_data = json.dumps(final, indent=4)

        # Send JSON data to server at port 5000 using a POST request
        url = 'http://localhost:5000/receive-data'  # Replace with actual endpoint if needed
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)

        if response.status_code == 200:
            print("Data successfully sent to the server!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

# Run the async function
asyncio.run(access_table())
