import pandas as pd
from playwright.sync_api import sync_playwright

# Start Playwright
with sync_playwright() as p:
    # Launch the browser (headless=True to run in background)
    browser = p.chromium.launch(headless=False)
    df=[]
    # Open a new page
    page = browser.new_page()
    
    # Navigate to the page with the table
    page.goto('https://www.screener.in/screens/319814/fundamentally-strong-undervalued-stocks/?page=1')

    # Wait for the specific table to load (increase timeout if needed)
    page.wait_for_selector('table.data-table.text-nowrap', timeout=60000)  # Wait 60 seconds max

    # Extract the table rows
    rows = page.query_selector_all('table.data-table.text-nowrap tbody tr')

    # Prepare data storage
    table_data = []

    # Loop over each row and extract cell data
    for row in rows:
        columns = row.query_selector_all('td')
        row_data = [col.inner_text().strip() for col in columns]
        table_data.append(row_data)

    # Close the browser
    browser.close()

    # Define headers (based on the table structure in your image)
    headers = [
        "S.No", "Name", "CMP Rs.", "P/E", "Market Cap Rs.Cr.", "Div Yld %","NP Qtr Rs.Cr.", "Qtr Profit Var %", "Sales Qtr Rs.Cr.", "Qtr Sales Var %",
        "ROCE %", "PEG", "ROE %","DEBT/EQ"
    ]
    
    for i in table_data:
        try:
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
                headers[10]:i[10],
                headers[11]:i[11],
                headers[12]:i[12],
                headers[13]:i[13],
            }
            df.append(data)
            
        except Exception as row_error:
            print(f"Error processing row: {row_error}")
            continue  # Skip to the next row if an error occurs    
        

    print(df)