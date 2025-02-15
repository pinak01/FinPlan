# AI-Driven Financial Planner

## Overview

The AI-Driven Financial Planner is a comprehensive tool designed to help individuals optimize their financial strategies by leveraging artificial intelligence. The planner assists users in areas such as tax saving, investment planning, stock portfolio restructuring, and AI-based stock prediction. By integrating user-specific data, market trends, and video inputs, the financial planner delivers tailored advice to meet diverse financial goals. This application provides detailed insights into taxes, smart investments, and stock management, enabling users to make informed decisions in an ever-evolving financial landscape.



# **Features:**

## Stock Portfolio Restructuring:(Our Main USP)

Offers AI-based portfolio analysis and restructuring to optimize returns based on real-time market conditions and user preferences.
Assists in building diversified portfolios through a variety of strategies, such as the Coffee Can or 60-40 approach.
Recommends stocks or sectors to focus on, based on user objectives, market performance, and risk appetite.

## AI Model for Stock Prediction (via Video Inputs):

Integrates AI models to predict stock performance based on user-provided videos.
Extracts key data points from the video (e.g., market news, expert analysis, industry trends) and converts it into actionable insights.
Offers stock suggestions and restructuring strategies based on the predictions derived from the video content.

## Tax Saving Advisor:

Provides personalized tax-saving strategies based on Section 80C, 80D, 80E, and other relevant deductions.
Compares tax liabilities under the old and new tax regimes, suggesting the most beneficial route.
Recommends additional tax-saving investments such as ELSS, PPF, and NPS, providing summaries and investment options.

## Investment Planner:

Helps users plan for significant purchases (like homes or cars) by calculating how long it will take to reach financial goals based on current income, monthly savings, and various investment avenues.
Recommends optimal investments based on user input, risk tolerance (low, medium, high), and projected returns.
Analyzes the time saved by making specific investments and suggests strategies for reaching goals faster.

# Key Technologies:

**Artificial Intelligence & Machine Learning:**

Uses generative AI to predict stock market trends and investment opportunities.
Analyzes video inputs with Natural Language Processing (NLP) to extract insights and generate recommendations.

**Enhanced Monte Carlo Simulation for Portfolio Performance**:
Simulates portfolio performance based on user-defined asset allocations.
Provides key metrics like Time-Weighted Rate of Return (TWRR), Sharpe Ratio, expected annual returns, and correlation between assets.
Using LSTM for historical data prediction to further enhance the accuracy of the simulation.

**Data Analytics:**

Processes financial data, market trends, and investment history to deliver personalized financial recommendations.
Implements algorithms to analyze the impact of various tax-saving investments, stock market patterns, and savings strategies.

# Taxation Frameworks:

Uses Indian tax laws and regulations (e.g., Sections 80C, 80D, 80CCD, and 24 of the Income Tax Act) to offer compliant tax-saving options.
How It Works

## User Input:

The user inputs their income, savings, financial goals, and risk tolerance.
The program prompts the user to provide details about their current investments and desired investment options.

For stock prediction, the user uploads a video containing relevant financial news or expert analysis.

# Sample output for stock prediction:

![image](https://github.com/user-attachments/assets/a5343aae-8552-46d0-ab99-0d88eccdb8ba)
![image](https://github.com/user-attachments/assets/cce23e7f-df5c-4fe4-b430-d189ab289d3c)

## AI-Driven Analysis:

The program processes user inputs to predict tax savings, investment returns, and stock market trends.
AI models analyze the video to derive stock-related insights, offering recommendations for portfolio restructuring or new stock purchases.

## Financial Recommendations:

Based on analysis, the program suggests tailored tax-saving plans, investment portfolios, and stocks with potential for growth.
Provides step-by-step guidance on how to invest, the time required to reach financial goals, and the impact of stock investments on overall timelines.

# Setup & Installation

Prerequisites:
Python 3.x
Required Python Libraries:
pandas
numpy
scikit-learn
tensorflow (for AI-based models)
YOLOv8 (for video and text processing)
seaborn

# Installation:

Clone the Repository:
git clone <repository-link>
mpm start

## Install Dependencies:

pip install -r requirements.txt

## Risk Profile Adjustments:

Customise the risk tolerance levels in the stock_recommendation() function to provide more granular recommendations.

## AI Model:

Replace or retrain the AI model used for stock prediction to improve accuracy.

## Tax Framework:

Add more tax-related features, such as deductions under international tax laws, if necessary.

# Future Enhancements:

**Real-time Market Data Integration:**
Integrate APIs from financial data providers to offer up-to-date stock and market trends.

**User Financial Profiles:**
Store user data to provide historical analysis and future predictions based on previous financial behaviour.

**Expanded Investment Options:**
Extend the investment recommendations to include mutual funds, bonds, and international stocks.

**Enhanced Video Processing:**
Improve video processing capabilities to support multiple languages and more detailed market analysis.

**Contributing:**
Feel free to contribute by submitting issues or pull requests to enhance the project!

# License

This project is licensed under the MIT License.
