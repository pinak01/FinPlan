from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

data_store = []  # To hold the data sent by the Python scraper

# Route to receive data via POST request
@app.route('/bulk-deal', methods=['POST'])
def receive_data():
    data = request.get_json()  # Get JSON data from the POST request
    global data_store
    data_store = data  # Store the received data
    return jsonify({'message': 'Data received successfully'}), 200

# Route to fetch data via GET request (for the browser)
@app.route('/get-data', methods=['GET'])
def get_data():
    global data_store
    return jsonify(data_store)  # Send the stored data as JSON


if __name__ == '__main__':
    app.run(port=5001)
