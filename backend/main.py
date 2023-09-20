
# backend/main.py

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from .cloud_connectors import oracle, azure
from .analysis import analyze_data
from .recommendations import generate_recommendations
from .forecasting import forecast_expenses

app = Flask(__name__)

# Create a database engine
engine = create_engine('sqlite:///cloud_data.db')

@app.route('/connect', methods=['POST'])
def connect():
    platform = request.json['platform']
    credentials = request.json['credentials']

    if platform == 'oracle':
        oracle.connect(credentials)
    elif platform == 'azure':
        azure.connect(credentials)
    else:
        return jsonify({'error': 'Invalid platform'}), 400

    return jsonify({'message': 'Connected successfully'}), 200

@app.route('/analyze', methods=['GET'])
def analyze():
    data = oracle.get_data() + azure.get_data()
    analysis = analyze_data(data)
    return jsonify(analysis), 200

@app.route('/recommend', methods=['GET'])
def recommend():
    data = oracle.get_data() + azure.get_data()
    recommendations = generate_recommendations(data)
    return jsonify(recommendations), 200

@app.route('/forecast', methods=['GET'])
def forecast():
    data = oracle.get_data() + azure.get_data()
    forecast = forecast_expenses(data)
    return jsonify(forecast), 200

if __name__ == '__main__':
    app.run(debug=True)

