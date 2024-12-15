from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import statistics

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://user1:asdfsdfdzc13reqfvdf@cluster0.cve6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['temperature_data_db']
collection = db['temperature_data_collection']


@app.route('/')
def home():
    """Serve web page for visualizing sensor data."""
    return render_template('index.html')


@app.route('/temperature-data/<sensor>', methods=['GET'])
def get_temperature_data(sensor):
    """Fetch temperature data for a specific sensor."""
    topic = f"senzor_{sensor}/temperatura"
    data = list(collection.find({"topic": topic}, {"_id": 0, "temperature": 1, "timestamp": 1}))

    if not data:
        return jsonify({"error": f"No data available for {sensor}"}), 404

    return jsonify(data)


@app.route('/average-temperature/<sensor>', methods=['GET'])
def average_temperature(sensor):
    """Calculate the average temperature for a specific sensor."""
    topic = f"senzor_{sensor}/temperatura"
    data = list(collection.find({"topic": topic}, {"_id": 0, "temperature": 1}))

    if not data:
        return jsonify({"error": f"No data available for {sensor}"}), 404

    temperatures = [entry['temperature'] for entry in data]
    average = statistics.mean(temperatures)

    return jsonify({"average_temperature": average, "total_entries": len(temperatures)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
