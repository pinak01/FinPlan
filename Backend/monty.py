import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

# Function to simulate portfolio performance
def monte_carlo_simulation(initial_investment, stocks, num_simulations=100, num_days=252):
    # Fetch historical data for the stocks
    stock_data = yf.download(list(stocks.keys()), start='2020-01-01', end='2023-01-01')
    stock_data['Adj Close'] = stock_data['Adj Close'].ffill()
    # Calculate daily returns
    daily_returns = stock_data['Adj Close'].pct_change().dropna()

    # Initialize an array to store end balances
    end_balances = []

    for _ in range(num_simulations):
        portfolio_value = initial_investment
        portfolio_values = [portfolio_value]

        for day in range(num_days):
            # Randomly select a day from the historical data
            random_day = np.random.choice(daily_returns.index, size=1)[0]
            daily_portfolio_return = sum(stocks[stock] * daily_returns.loc[random_day][stock] for stock in stocks)
            portfolio_value *= (1 + daily_portfolio_return)
            portfolio_values.append(portfolio_value)

        end_balances.append(portfolio_value)

        # Plotting the portfolio balance over time
        plt.plot(portfolio_values, alpha=0.1, color='blue')

    # Performance Summary
    end_balances = np.array(end_balances)
    nominal_returns = (end_balances / initial_investment) - 1
    real_returns = nominal_returns  # Adjust this if you have inflation data

    # Percentiles for performance metrics
    percentiles = [10, 25, 50, 75, 90]
    performance_summary = {}

    for p in percentiles:
        performance_summary[p] = {
            "Time Weighted Rate of Return (nominal)": np.percentile(nominal_returns, p) * 100,
            "Portfolio End Balance (nominal)": np.percentile(end_balances, p),
            "Annual Mean Return (nominal)": np.mean(nominal_returns) * 100,
            "Annualized Volatility": np.std(nominal_returns) * np.sqrt(num_days) * 100,
            "Sharpe Ratio": (np.mean(nominal_returns) / np.std(nominal_returns)) * np.sqrt(num_days),
            "Sortino Ratio": (np.mean(nominal_returns) / np.std(nominal_returns[nominal_returns < 0])) * np.sqrt(num_days) if np.std(nominal_returns[nominal_returns < 0]) != 0 else 0
        }

    # Output the enhanced performance summary
    print("Performance Summary:")
    print("Percentile\t" + "\t".join([f"{p}th" for p in percentiles]))
    for key in performance_summary[10].keys():
        print(f"{key}\t" + "\t".join([f"{performance_summary[p][key]:.2f}" for p in percentiles]))

    # Plotting Portfolio End Balance Histogram
    plt.figure()
    plt.hist(end_balances, bins=30, alpha=0.7, color='orange')
    plt.title('Portfolio End Balance Histogram')
    plt.xlabel('End Balance')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

    # Simulated Assets - Correlations and Returns
    returns_df = daily_returns[stocks.keys()]
    correlations = returns_df.corr()
    print("Simulated Assets Correlation Matrix:")
    print(correlations)

    # Plotting the correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Simulated Assets Correlation Matrix')
    plt.show()

# Example stocks and their allocations
stocks = {
    'AAPL': 0.5,  # 50% allocation
    'MSFT': 0.3,  # 30% allocation
    'GOOGL': 0.2  # 20% allocation
}

# Set initial investment amount
initial_amount = 10000  # Example initial investment of $10,000

# Run the simulation
monte_carlo_simulation(initial_amount, stocks)




# @app.route('/monty', methods=['POST'])
# async def monty_route():
    
#     try:
#         data = request.get_json()
#         tickername = data.get('tickername')
#         allocation = data.get('allocation')
#         initial_amt = data.get('initialamt')

#         if not tickername:
#             return jsonify({"error": "Required is required"}), 400
        
#         if not allocation:
#             return jsonify({"error": "Current is required"}), 400
        
#         if not initial_amt:
#             return jsonify({"error": "Initial Amount is required"}), 400
#         print(tickername,allocation,initial_amt)
#         stocks={}
#         for i in range(len(tickername)):
#             stocks[tickername[i]]=float(allocation[i])
#         print(stocks)
#         stock1 = {
#             'AAPL': 0.5,  # 50% allocation
#             'MSFT': 0.3,  # 30% allocation
#             'GOOGL': 0.2  # 20% allocation
#         }
#         num_simulations=100
#         num_days=252
#         initial_investment=float(initial_amt)
#         stocks=stock1

#         stock_data = yf.download(list(stocks.keys()), start='2020-01-01', end='2023-01-01')
#         stock_data['Adj Close'] = stock_data['Adj Close'].ffill()
#         # Calculate daily returns
#         daily_returns = stock_data['Adj Close'].pct_change().dropna()

#         # Initialize an array to store end balances
#         end_balances = []

#         for _ in range(num_simulations):
#             portfolio_value = initial_investment
#             portfolio_values = [portfolio_value]

#             for day in range(num_days):
#                 # Randomly select a day from the historical data
#                 random_day = np.random.choice(daily_returns.index, size=1)[0]
#                 daily_portfolio_return = sum(stocks[stock] * daily_returns.loc[random_day][stock] for stock in stocks)
#                 portfolio_value *= (1 + daily_portfolio_return)
#                 portfolio_values.append(portfolio_value)

#             end_balances.append(portfolio_value)

#             # Plotting the portfolio balance over time
#             plt.plot(portfolio_values, alpha=0.1, color='blue')

#         # Performance Summary
#         end_balances = np.array(end_balances)
#         nominal_returns = (end_balances / initial_investment) - 1
#         real_returns = nominal_returns  # Adjust this if you have inflation data

#         # Percentiles for performance metrics
#         percentiles = [10, 25, 50, 75, 90]
#         performance_summary = {}

#         for p in percentiles:
#             performance_summary[p] = {
#                 "Time Weighted Rate of Return (nominal)": np.percentile(nominal_returns, p) * 100,
#                 "Portfolio End Balance (nominal)": np.percentile(end_balances, p),
#                 "Annual Mean Return (nominal)": np.mean(nominal_returns) * 100,
#                 "Annualized Volatility": np.std(nominal_returns) * np.sqrt(num_days) * 100,
#                 "Sharpe Ratio": (np.mean(nominal_returns) / np.std(nominal_returns)) * np.sqrt(num_days),
#                 "Sortino Ratio": (np.mean(nominal_returns) / np.std(nominal_returns[nominal_returns < 0])) * np.sqrt(num_days) if np.std(nominal_returns[nominal_returns < 0]) != 0 else 0
#             }

#         # Output the enhanced performance summary
#         print("Performance Summary:")
#         print("Percentile\t" + "\t".join([f"{p}th" for p in percentiles]))
#         for key in performance_summary[10].keys():
#             print(f"{key}\t" + "\t".join([f"{performance_summary[p][key]:.2f}" for p in percentiles]))

#         # Plotting Portfolio End Balance Histogram
#         plt.figure()
#         plt.hist(end_balances, bins=30, alpha=0.7, color='orange')
#         plt.title('Portfolio End Balance Histogram')
#         plt.xlabel('End Balance')
#         plt.ylabel('Frequency')
#         plt.grid()
#         plt.show()

#         # Simulated Assets - Correlations and Returns
#         returns_df = daily_returns[stocks.keys()]
#         correlations = returns_df.corr()
#         print("Simulated Assets Correlation Matrix:")
#         print(correlations)

#         # Plotting the correlation matrix
#         plt.figure(figsize=(8, 6))
#         sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
#         plt.title('Simulated Assets Correlation Matrix')
#         plt.show()
            


    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500