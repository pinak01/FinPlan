from flask import Flask, jsonify
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
import requests
import plotly.io as pio
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)


# Set the default renderer to 'browser' to generate the chart
pio.renderers.default = 'browser'

# Define the stock ticker and fetch data from yfinance
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

# Define API route
@app.route('/get-chart', methods=['GET'])
def get_chart():
    try:
        company_name = 'Aartech Solonics Limited'
        stock_ticker = get_ticker(company_name)

        # Fetch the historical stock data
        hists = yf.download(stock_ticker, period='1y')  # Download last year's data

        # Filter data for the last month
        one_month_ago = datetime.now() - timedelta(days=30)  # Change to 30 days for the last month
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
