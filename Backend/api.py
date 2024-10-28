import os
from groq import Groq
from flask import Flask, jsonify,request
import json
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)
consumer=[]
required_stocks=[]
current_stocks=[]

def apigroq():
    # Initialize the Groq client
    client = Groq(
        api_key=("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")
    )
    global consumer
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
        consumer.append(sentence)

@app.route('/api', methods=['POST'])
def consumer_stocks_route():
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

        apigroq()
        global consumer
        return jsonify(consumer)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(port=5002)



