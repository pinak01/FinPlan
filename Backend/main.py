import asyncio
import json
import io
import base64
from playwright.async_api import async_playwright
from flask import Flask, jsonify,request
from flask_cors import CORS
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
import requests
import plotly.io as pio
import requests
from playwright.sync_api import sync_playwright
from groq import Groq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# FOR BULK DATA
async def access_table():
    scraped_data = []  # Clear previous data before starting the scrape

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True if you want to run in the background
        page = await browser.new_page()

        # Navigate to the page containing the table
        await page.goto('https://www.moneycontrol.com/stocks/marketstats/bulk-deals/nse/')
        await asyncio.sleep(60)

        # Select the table
        await page.wait_for_selector('.fidi_tbl.MB20.bulkdls1.CTR tbody')
        
        rows = await page.query_selector_all('.fidi_tbl.MB20.bulkdls1.CTR tbody tr')
        
        # Debugging: Log how many rows were found
        print(f"Found {len(rows)} rows.")

        # Define the keys for the table data
        keys = ["Date", "Company", "Client", "Trans", "Quantity", "Traded", "Closed"]

        # Loop through each row
        for row in rows:
            cells = await row.query_selector_all('td')
            
            if len(cells) == len(keys):  # Make sure row has the correct number of cells
                obj = {}
                for i, cell in enumerate(cells):
                    cell_text = await cell.text_content()
                    obj[keys[i]] = cell_text.strip()  # Assign cell content to the corresponding key
                scraped_data.append(obj)
            else:
                print(f"Skipping row with {len(cells)} cells (expected {len(keys)}).")
        
        # Close the browser
        await browser.close()

        # If no data is found, log an error
        if not scraped_data:
            print("No data found in the table.")
            return
        
        json_data = json.dumps(scraped_data, indent=4)

        # Send JSON data to server at port 5000 using a POST request
        url = 'http://localhost:5001/bulk-deal'  # Replace with actual endpoint if needed
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)

        if response.status_code == 200:
            print("Data successfully sent to the server!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

# asyncio.run(access_table())

# FOR GRAPH
def get_ticker(company_name):
    yfinance_url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance_url, params=params, headers={'User-Agent': user_agent})
    if res.status_code == 200:
        data = res.json()
        if data['quotes']:
            return data['quotes'][0]['symbol']
        else:
            raise ValueError("No quotes found for the given company name.")
    else:
        raise ConnectionError("Failed to connect to Yahoo Finance API.")
    
@app.route('/get-chart', methods=['POST'])
def get_chart():
    try:
        data = request.get_json()
        company_name = data.get('company_name')  # Get the company name from the request body

        if not company_name:
            return jsonify({"error": "Company name is required"}), 400

        stock_ticker = get_ticker(company_name)

        # Fetch the historical stock data
        hists = yf.download(stock_ticker, period='5d')  # Download last year's data

        # Filter data for the last month
        one_month_ago = datetime.now() - timedelta(days=30)
        temp_df = hists[hists.index >= one_month_ago].copy()

        # Create the candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=temp_df.index,
                                             open=temp_df['Open'],
                                             high=temp_df['High'],
                                             low=temp_df['Low'],
                                             close=temp_df['Close'])])

        # Update layout with customizations
        fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=300,
            paper_bgcolor="LightSteelBlue",
            title=f'Candlestick chart for {company_name}'
        )

        # Convert the figure to JSON
        chart_json = fig.to_json()

        # Return the chart as JSON response
        return jsonify(chart_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# FOR MONEY-MARKET
moneymarket=[]
async def money_market():
    global moneymarket  # Clear previous data before starting the scrape

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=True if you want to run in the background
        page = await browser.new_page()

        # Navigate to the page containing the table
        await page.goto('https://www.etmoney.com/mutual-funds/debt/money-market/58')
        await asyncio.sleep(3)

        # Select the table
        await page.wait_for_selector('.performing-data')
        
        name = await page.query_selector_all('.fund-name.scheme-name')
        fundAmount= await page.query_selector_all('.fund-size .fund-amount')
        returns= await page.query_selector_all('.return-list.sip-returns.top-row .item-value.percent.green-text.period-1825.active')

        # Debugging: Log how many rows were found
        print(f"Found {len(name)} {len(fundAmount)} {len(returns)} rows.")


        # # Loop through each row
        for row in range(0,len(returns)):
            data={
                "ShareName": await name[row].text_content(),
                "FundSize": await fundAmount[row].text_content(),
                "Return": await returns[row].text_content()
            }
            moneymarket.append(data)

        
        # Close the browser
        await browser.close()

        # If no data is found, log an error
        if not moneymarket:
            print("No data found in the MoneyMarket.")
            return

@app.route('/money-market', methods=['GET'])
def get_market_money():
    global moneymarket
    moneymarket=[]
    asyncio.run(money_market())
    
    return jsonify(moneymarket)  # Send the stored data as JSON

# FOR LARGE CAP
funds_json = []
def large_cap():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/mutual-funds/category/best-large-cap-mutual-funds")

        # Wait for the content to load
        page.wait_for_selector('.stfs4Anchor')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.stfs4Anchor')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        global funds_json
        i = 0
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "ShareName": details1[68 + i],
                "Risk": details1[69 + i],
                "Return": details1[70 + i],
                "FundSize": details1[72 + i][1:]
            }
            funds_json.append(fund_data)
            i += 6

        # Close the browser
        browser.close()

@app.route('/large-cap', methods=['GET'])
def largecap():
    global funds_json
    funds_json=[]
    large_cap()
    
    return jsonify(funds_json)  # Send the stored data as JSON

# FOR LIQUID
liquid=[]
def liquidfunc():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/mutual-funds/category/best-liquid-mutual-funds")

        # Wait for the content to load
        page.wait_for_selector('.stfs4Anchor')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.stfs4Anchor')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        global liquid
        i = 0
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "ShareName": details1[68 + i],
                "Risk": details1[69 + i],
                "Return": details1[70 + i],
                "FundSize": details1[72 + i][1:]
            }
            liquid.append(fund_data)
            i += 6

        # Close the browser
        browser.close()

@app.route('/liquid', methods=['GET'])
def liquidroute():
    global liquid
    liquid=[]
    liquidfunc()
    
    return jsonify(liquid)  # Send the stored data as JSON


# FOR MID-CAP
midcap=[]
def mid_cap():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/mutual-funds/category/best-mid-cap-mutual-funds")

        # Wait for the content to load
        page.wait_for_selector('.stfs4Anchor')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.stfs4Anchor')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        # Print or return the scraped data
        global midcap
        i = 0
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "ShareName": details1[68 + i],
                "Risk": details1[69 + i],
                "Return": details1[70 + i],
                "FundSize": details1[72 + i][1:]
            }
            midcap.append(fund_data)
            i += 6

        # Close the browser
        browser.close()

@app.route('/mid-cap', methods=['GET'])
def midcaproute():
    global midcap
    midcap=[]
    mid_cap()
    
    return jsonify(midcap)  # Send the stored data as JSON

#FOR REAL-ESTATE
realestate=[]
def real_estate():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/stocks/sectors/real-estate")

        # Wait for the content to load
        page.wait_for_selector('.st76SymbolName')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.st76SymbolName')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.st76DivSec')
        close=page.query_selector_all('.st76Pad16')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        close1=[close1.inner_text() for close1 in close]
        i = 0
        j=1
        global realestate

        # Build the data structure for JSON
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund,
                "close": close1[i][1:],
                "market Cap in cr": close1[j][1:]
            }
            realestate.append(fund_data)
            i += 2
            j=j+2

        # Close the browser
        browser.close()

@app.route('/real-estate', methods=['GET'])
def realestateroute():
    global realestate
    realestate=[]
    real_estate()
    
    return jsonify(realestate)  # Send the stored data as JSON

#FOR SHORT-FUND
shortfund=[]
def short_fund():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
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
        global shortfund
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
            shortfund.append(fund_data)
            i += 6

        # Close the browser
        browser.close()

@app.route('/short-fund', methods=['GET'])
def shortfundroute():
    global shortfund
    shortfund=[]
    short_fund()
    
    return jsonify(shortfund)  # Send the stored data as JSON

#FOR SMALL-CAP
smallcap=[]
def small_cap():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://groww.in/mutual-funds/category/best-small-cap-mutual-funds")

        # Wait for the content to load
        page.wait_for_selector('.stfs4Anchor')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('.stfs4Anchor')  # Adjust the selector based on the fund name's CSS class
        details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        details1=  [detail.inner_text() for detail in details]
        global smallcap
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
            smallcap.append(fund_data)
            i += 6

        browser.close()

@app.route('/small-cap', methods=['GET'])
def smallcaproute():
    global smallcap
    smallcap=[]
    small_cap()
   
    return jsonify(smallcap)  # Send the stored data as JSON        


#FOR VOLATILE
volatile=[]
def volatile_func():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
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
        global volatile

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
            volatile.append(fund_details)
            i += 10


        # Close the browser
        browser.close()

@app.route('/volatile', methods=['GET'])
def volatileroute():
    global volatile
    volatile=[]
    volatile_func()
    
    return jsonify(volatile)  # Send the stored data as JSON

# FOR MUNICIPAL
municipal=[]
def municipal_func():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.sebi.gov.in/statistics/municipalbonds.html")

        # Wait for the content to load
        page.wait_for_selector('.org-table-1')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('td')  # Adjust the selector based on the fund name's CSS class
        #details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        #details1=  [detail.inner_text() for detail in details]
        global municipal
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund_list[i],
                "Date_of_issue":fund_list[i+1],
                "Date_of_maturity":fund_list[i+2],
                "Amount_in_Cr":fund_list[i+3],
                "Tenure_in_yrs":fund_list[i+5]
            }
            i=i+8
            if (idx==10):
                break
            municipal.append(fund_data)

        # Close the browser
        browser.close()

@app.route('/municipal', methods=['GET'])
def municipalroute():
    global municipal
    municipal=[]
    municipal_func()
    
    return jsonify(municipal)  # Send the stored data as JSON

#FOR LONG-TERM-BONDS
longtermbonds=[]
def long_term_bonds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.sebi.gov.in/statistics/municipalbonds.html")

        # Wait for the content to load
        page.wait_for_selector('.org-table-1')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('td')  # Adjust the selector based on the fund name's CSS class
        #details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        #details1=  [detail.inner_text() for detail in details]
        global longtermbonds
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "fund": fund_list[i],
                "Date_of_issue":fund_list[i+1],
                "Date_of_maturity":fund_list[i+2],
                "Amount_in_Cr":fund_list[i+3],
                "Tenure_in_yrs":fund_list[i+5]
            }
            i=i+8
            if (idx==10):
                break
            longtermbonds.append(fund_data)

        # Close the browser
        browser.close()

@app.route('/long-term-bonds', methods=['GET'])
def longtermbondsroute():
    global longtermbonds
    longtermbonds=[]
    long_term_bonds()
    
    return jsonify(longtermbonds)  # Send the stored data as JSON

# FOR CORPORATE BONDS
corporatebonds=[]
def corporate_bonds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.sebi.gov.in/statistics/municipalbonds.html")

        # Wait for the content to load
        page.wait_for_selector('.org-table-1')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('td')  # Adjust the selector based on the fund name's CSS class
        #details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        #details1=  [detail.inner_text() for detail in details]
        global corporatebonds
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund_list[i],
                "Date_of_issue":fund_list[i+1],
                "Date_of_maturity":fund_list[i+2],
                "Amount_in_Cr":fund_list[i+3],
                "Tenure_in_yrs":fund_list[i+5]
            }
            i=i+8
            if (idx==10):
                break
            corporatebonds.append(fund_data)

        # Close the browser
        browser.close()

@app.route('/corporate-bonds', methods=['GET'])
def corporatebondsroute():
    global corporatebonds
    corporatebonds=[]
    corporate_bonds()
    
    return jsonify(corporatebonds)  # Send the stored data as JSON

# FOR SHORT TERM BONDS
shorttermbonds=[]
def short_term_bonds():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
        page = browser.new_page()

        # Navigate to the Groww page
        page.goto("https://www.sebi.gov.in/statistics/municipalbonds.html")

        # Wait for the content to load
        page.wait_for_selector('.org-table-1')  # Assuming the fund name has this class, adjust as needed

        # Scrape the data
        fund_names = page.query_selector_all('td')  # Adjust the selector based on the fund name's CSS class
        #details = page.query_selector_all('.contentPrimary.bodyBase')
        # Collect the fund names
        fund_list = [fund.inner_text() for fund in fund_names]
        #details1=  [detail.inner_text() for detail in details]
        global shorttermbonds
        i = 1
        for idx, fund in enumerate(fund_list, 1):
            fund_data = {
                "index": idx,
                "fund": fund_list[i],
                "Date_of_issue":fund_list[i+1],
                "Date_of_maturity":fund_list[i+2],
                "Amount_in_Cr":fund_list[i+3],
                "Tenure_in_yrs":fund_list[i+5]
            }
            i=i+8
            if (idx==10):
                break
            shorttermbonds.append(fund_data)

        # Close the browser
        browser.close()

@app.route('/short-term-bonds', methods=['GET'])
def shorttermbondsroute():
    global shorttermbonds
    shorttermbonds=[]
    short_term_bonds()
    
    return jsonify(shorttermbonds)  # Send the stored data as JSON

# FOR ETF
etf=[]
async def etf_func(playwright):
    # Launch the browser
    global etf
    browser = await playwright.chromium.launch(headless=True)  # Set headless=True to run in the background
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
    etf = etf_data
    # Close the browser
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await etf_func(playwright)


@app.route('/etf', methods=['GET'])
def etf_route():
    global etf
    etf=[]
    asyncio.run(main())
    
    return jsonify(etf)


# FOR GOLD ETF
goldetf=[]
async def gold_etf(playwright):
    # Launch the browser
    global goldetf
    browser = await playwright.chromium.launch(headless=True)  # Set headless=True to run in the background
    page = await browser.new_page()

    # Navigate to the page with the ETF table (replace with the actual URL)
    await page.goto('https://groww.in/etfs?filter=Gold')  # Replace with the actual URL

    # Wait for the table to load
    await page.wait_for_selector('table.tb10Table')

    # Extract data from each row of the ETF table
    goldetf_data = await page.evaluate('''() => {
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

    goldetf = goldetf_data
    # Close the browser
    await browser.close()


async def main1():
    async with async_playwright() as playwright:
        await gold_etf(playwright)


@app.route('/gold-etf', methods=['GET'])
def gold_etf_route():
    global goldetf
    goldetf=[]
    asyncio.run(main1())
    
    return jsonify(goldetf)

# FOR CYCLICAL STOCKS
cyclicalstocks = []
def cyclical_stocks():
    with sync_playwright() as p:
        global cyclicalstocks
        browser = None
        try:
            # Launch the browser
            browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
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

        except Exception as browser_error:
            print(f"An error occurred while scraping: {browser_error}")

        finally:
            if browser:
                browser.close()  # Ensure the browser closes even if an error occurs

@app.route('/cyclical-stocks', methods=['GET'])
def cyclical_stocks_route():
    global cyclicalstocks
    cyclicalstocks=[]
    cyclical_stocks()
    
    return jsonify(cyclicalstocks)

# FOR DIVIDEND
dividend = []
def dividend_stocks():
    with sync_playwright() as p:
        global dividend
        browser = None
        try:
            # Launch the browser
            browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
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
                        dividend.append(data)


                    except Exception as row_error:
                        print(f"Error processing row {j}: {row_error}")
                        continue  # Skip to the next row if an error occurs

        except Exception as browser_error:
            print(f"An error occurred while scraping: {browser_error}")

        finally:
            if browser:
                browser.close()  # Ensure the browser closes even if an error occurs

@app.route('/dividend-stocks', methods=['GET'])
def dividend_stocks_route():
    global dividend
    dividend=[]
    dividend_stocks()
    
    return jsonify(dividend)


# FOR GROWTH
growth=[]
def growth_stocks():
    with sync_playwright() as p:
        # Launch the browser (Chromium, Firefox, or WebKit)
        global growth
        browser = p.chromium.launch(headless=True)
        
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
            growth.append(data)

@app.route('/growth-stocks', methods=['GET'])
def growth_stocks_route():
    global growth
    growth=[]
    growth_stocks()
    
    return jsonify(growth)


# FOR BLUE CHIP
bluechip = []
def bluechip_stocks():
    with sync_playwright() as p:
        global bluechip
        browser = None
        try:
            # Launch the browser
            browser = p.chromium.launch(headless=True)  # Set headless=True if you want to see the browser
            page = browser.new_page()

            # Navigate to the Screener page
            page.goto("https://www.etmoney.com/stocks/market-data/bluechip-stocks/38")

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
                            "Volume": fund_data[5].text_content(),
                        }
                        bluechip.append(data)


                    except Exception as row_error:
                        print(f"Error processing row {j}: {row_error}")
                        continue  # Skip to the next row if an error occurs

        except Exception as browser_error:
            print(f"An error occurred while scraping: {browser_error}")

        finally:
            if browser:
                browser.close()  # Ensure the browser closes even if an error occurs

@app.route('/bluechip-stocks', methods=['GET'])
def bluechip_stocks_route():
    global bluechip
    bluechip=[]
    bluechip_stocks()
    
    return jsonify(bluechip)


# FOR VALUE STOCKS
value=[]
def value_stocks():
    # Start Playwright
    with sync_playwright() as p:
        # Launch the browser (headless=True to run in background)
        global value
        browser = p.chromium.launch(headless=True)
        
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
                value.append(data)
                
            except Exception as row_error:
                print(f"Error processing row: {row_error}")
                continue  # Skip to the next row if an error occurs    
            
@app.route('/value-stocks', methods=['GET'])
def value_stocks_route():
    global value
    value=[]
    value_stocks()
    
    return jsonify(value)

# FOR SECTOR STOCKS
sector=[]
async def sector_stocks(playwright):
    # Launch the browser
    global sector
    browser = await playwright.chromium.launch(headless=True)  # Set headless=True to run in the background
    page = await browser.new_page()

    # Navigate to the page with the ETF table (replace with the actual URL)
    await page.goto('https://groww.in/stocks/sectors')  # Replace with the actual URL

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
    sector = etf_data
    # Close the browser
    await browser.close()


async def main3():
    async with async_playwright() as playwright:
        await sector_stocks(playwright)

@app.route('/sector-stocks', methods=['GET'])
def sector_stock_route():
    global sector
    sector=[]
    asyncio.run(main3())
    
    return jsonify(sector)


# FOR TECHNOLOGY STOCK
technology=[]
def technology_stocks():
    # Start Playwright
    with sync_playwright() as p:
        # Launch the browser (headless=True to run in background)
        global technology
        browser = p.chromium.launch(headless=True)
        
        # Open a new page
        page = browser.new_page()
        
        # Navigate to the page with the table
        page.goto('https://www.screener.in/company/compare/00000034/')

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
            "ROCE %"
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
                    headers[10]:i[10]
                }
                technology.append(data)
                
            except Exception as row_error:
                print(f"Error processing row: {row_error}")
                continue  # Skip to the next row if an error occurs    
            
@app.route('/tech-stocks', methods=['GET'])
def tech_stocks_route():
    global technology
    technology=[]
    technology_stocks()
    
    return jsonify(technology)


# FOR CONSUMER STOCK
consumer=[]
def consumer_stocks():
    # Start Playwright
    with sync_playwright() as p:
        # Launch the browser (headless=True to run in background)
        global consumer
        browser = p.chromium.launch(headless=True)
        
        # Open a new page
        page = browser.new_page()
        
        # Navigate to the page with the table
        page.goto('https://www.screener.in/company/1160/')

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
            "ROCE %"
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
                    headers[10]:i[10]
                }
                consumer.append(data)
                
            except Exception as row_error:
                print(f"Error processing row: {row_error}")
                continue  # Skip to the next row if an error occurs    
            
@app.route('/consumer-stocks', methods=['GET'])
def consumer_stocks_route():
    global consumer
    consumer=[]
    consumer_stocks()
    return jsonify(consumer)

# FOR TICKER
def ticker(company_name):
    yfinance_url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance_url, params=params, headers={'User-Agent': user_agent})
    if res.status_code == 200:
        data = res.json()
        if data['quotes']:
            return data['quotes'][0]['symbol']
        else:
            return company_name
    else:
        return company_name
    
@app.route('/get-ticker', methods=['POST'])
def get_tick():
    try:
        show=[]
        data = request.get_json()
        company_name = data.get('company_name')  # Get the company name from the request body
        print(company_name)
        if not company_name:
            return jsonify({"error": "Company name is required"}), 400

        for i in company_name:          
            stock_ticker = ticker(i)
            show.append(stock_ticker)   
        print(show)
        return jsonify(show)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#FOR GROQ API
groq=[]
required_stocks=[]
current_stocks=[]

def apigroq():
    # Initialize the Groq client
    client = Groq(
        api_key=("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")
    )
    global groq
    global required_stocks
    global current_stocks
    print(current_stocks)
    print(required_stocks)
    # Define the required stock categories and the current specific stocks in your portfolio
    # required_stocks = [
    #     "gold ETF", 
    #     "growth stocks", 
    #     "mid-cap stocks", 
    #     "large-cap stocks"
    # ]  # Replace with your required stock categories, focusing on the Indian market
    # current_stocks = ["RELIANCE", "TCS", "HDFCBANK"] 

    prompt_content = f"""
    You are an AI investment assistant. I will provide you with two lists:

    1. A list of required stock categories for my desired portfolio.
    2. A list of my current specific stocks in my portfolio.

    Your task is to:
    1. Match the specific stocks in my portfolio with their respective categories (e.g., AAPL might be in "large-cap stocks").
    2. Provide a detailed, informative message acknowledging the stocks I am currently invested in, explaining what role they play in my portfolio based on their categories.
    3. Identify which stock categories are missing from my portfolio based on the provided current stocks.
    4. DO NOT suggest specific stocks to buy. Simply identify the missing categories that need to be filled and provide guidance on why these categories are important to a balanced portfolio.
    5. Make every sentence as a point starting with star (dont end with star)
    6. Dont use any other extra star

    Required stock categories: {required_stocks}
    Current specific stocks: {current_stocks}

    Please provide an informative, detailed response.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_content,
            }
        ],
        model="llama3-8b-8192",
    )

    response_text=chat_completion.choices[0].message.content

    response_array = response_text.split("• ")

    # Optionally, remove any empty entries caused by splitting
    response_array = [sentence.strip() for sentence in response_array if sentence.strip()]

    for index, sentence in enumerate(response_array, 1):
        groq.append(sentence)

@app.route('/groq-api', methods=['POST'])
def groq_api_route():
    try:
        global required_stocks
        global current_stocks
        data = request.get_json()
        required_stocks = data.get('required')
        current_stocks = data.get('current')

        if not required_stocks:
            return jsonify({"error": "Required is required"}), 400
        
        if not current_stocks:
            return jsonify({"error": "Current is required"}), 400
        
        global groq
        groq=[]

        apigroq()
        
        return jsonify(groq)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# FOR MONTY
@app.route('/monty', methods=['POST'])
async def monty_route():
    try:
        data = request.get_json()
        tickername = data.get('tickername')
        allocation = data.get('allocation')
        initial_amt = data.get('initialamt')

        if not tickername:
            return jsonify({"error": "Required is required"}), 400

        if not allocation:
            return jsonify({"error": "Current is required"}), 400

        if not initial_amt:
            return jsonify({"error": "Initial Amount is required"}), 400

        stocks = {}
        for i in range(len(tickername)):
            stocks[tickername[i]] = float(allocation[i])

        num_simulations = 100
        num_days = 252
        initial_investment = float(initial_amt)

        # Fetch historical data for the stocks
        stock_data = yf.download(list(stocks.keys()), start='2020-01-01', end='2023-01-01')

        # Calculate daily returns
        daily_returns = stock_data['Adj Close'].pct_change().dropna()

        # Initialize an array to store end balances and daily portfolio returns
        end_balances = []
        all_portfolio_returns = []

        for _ in range(num_simulations):
            portfolio_value = initial_investment
            portfolio_values = [portfolio_value]
            daily_portfolio_returns = []

            for day in range(num_days):
                random_day = np.random.choice(daily_returns.index, size=1)[0]
                daily_portfolio_return = sum(stocks[stock] * daily_returns.loc[random_day][stock] for stock in stocks)
                portfolio_value *= (1 + daily_portfolio_return)
                portfolio_values.append(portfolio_value)
                daily_portfolio_returns.append(daily_portfolio_return)

            end_balances.append(portfolio_value)
            all_portfolio_returns.append(daily_portfolio_returns)

            # Plot portfolio balance over time and save to a base64 image
            plt.plot(portfolio_values, alpha=0.1, color='blue')

        # Convert the plot to a base64 image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        portfolio_image_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        img_buffer.close()
        plt.clf()  # Clear plot for next one

        # Performance Summary
        percentiles = [10, 25, 50, 75, 90]
        performance_summary = {}
        end_balances = np.array(end_balances)
        all_portfolio_returns = np.array(all_portfolio_returns)

        for p in percentiles:
            percentile_index = int(np.percentile(np.arange(num_simulations), p))
            portfolio_returns_percentile = all_portfolio_returns[percentile_index]
            nominal_return = (end_balances[percentile_index] / initial_investment) - 1
            annual_mean_return = np.mean(portfolio_returns_percentile) * 252
            annualized_volatility = np.std(portfolio_returns_percentile) * np.sqrt(252)
            sharpe_ratio = (annual_mean_return / annualized_volatility) if annualized_volatility != 0 else 0
            downside_volatility = np.std([r for r in portfolio_returns_percentile if r < 0]) * np.sqrt(252)
            sortino_ratio = (annual_mean_return / downside_volatility) if downside_volatility != 0 else 0

            performance_summary[p] = {
                "Time Weighted Rate of Return (nominal)": nominal_return * 100,
                "Portfolio End Balance (nominal)": end_balances[percentile_index],
                "Annual Mean Return (nominal)": annual_mean_return * 100,
                "Annualized Volatility": annualized_volatility * 100,
                "Sharpe Ratio": sharpe_ratio,
                "Sortino Ratio": sortino_ratio
            }

        # Plot and convert the portfolio end balance histogram to base64
        plt.hist(end_balances, bins=30, alpha=0.7, color='orange')
        plt.title('Portfolio End Balance Histogram')
        plt.xlabel('End Balance')
        plt.ylabel('Frequency')
        plt.grid()

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        balance_histogram_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        img_buffer.close()
        plt.clf()  # Clear plot

        # Plot correlation matrix and save as base64
        returns_df = daily_returns[stocks.keys()]
        correlations = returns_df.corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Simulated Assets Correlation Matrix')

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        correlation_matrix_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        img_buffer.close()
        plt.clf()

        # Return both base64 images and JSON data
        return jsonify({
            "performance_summary": performance_summary,
            "images": {
                "portfolio_balance_over_time": portfolio_image_base64,
                "portfolio_end_balance_histogram": balance_histogram_base64,
                "correlation_matrix": correlation_matrix_base64
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
   




if __name__ == '__main__':
    app.run(port=5000)
