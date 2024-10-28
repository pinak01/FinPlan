import pandas as pd
from playwright.sync_api import sync_playwright

# Start Playwright
with sync_playwright() as p:
    # Launch the browser (Chromium, Firefox, or WebKit)
    df=[]
    browser = p.chromium.launch(headless=False)
    
    # Open a new page
    page = browser.new_page()
    
    # Navigate to the page with the table
    page.goto('https://www.nseindia.com/market-data/volume-gainers-spurts')

    # Wait for the table to be loaded (optional, depending on how the page loads)
    page.wait_for_selector('#volumeGainerTable', timeout=60000) 

    # Extract the table rows
    rows = page.query_selector_all('#volumeGainerTable tbody tr')

    # Prepare data storage
    table_data = []

    # Loop over each row and extract cell data
    for row in rows:
        columns = row.query_selector_all('td')
        row_data = [col.inner_text().strip() for col in columns]
        table_data.append(row_data)

    # Close the browser
    browser.close()

    # Convert to a pandas DataFrame (assume headers based on your image)
    headers = ['Symbol', 'Security', 'Today Volume', '1 Week Avg. Volume', '1 week Change ', '2 Week Avg. Volume','2 week Change ','Today LTP','Today percent change','Today Turnover(Lakhs)']
    for i in table_data:
        data={
            headers[0]:i[0],
            headers[1]:i[1],
            headers[2]:i[2],
            headers[3]:i[3],
            headers[4]:i[4],
            headers[5]:i[5],
            headers[6]:i[6],
            headers[7]:i[7],
            headers[8]:i[8],
            headers[9]:i[9],
        }
        df.append(data)
    print(df)    



