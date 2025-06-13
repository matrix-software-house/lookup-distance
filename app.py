# app.py
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# CORS(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PORT = 5001

@app.route('/distance', methods=['GET'])
def get_distance():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # Check if both origin and destination are provided
    if not origin or not destination:
        return jsonify({ "error": "You must provide both origin and destination locations." }), 400

    # Construct the request URL for the Google Distance Matrix API
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={requests.utils.quote(origin)}"
        f"&destinations={requests.utils.quote(destination)}"
        f"&key={GOOGLE_API_KEY}&mode=walking"
    )

    try:
        # Make the request to the Google API
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.RequestException:
        return jsonify({ "error": "Error while accessing Google API." }), 500

# Start the Flask server
if __name__ == '__main__':
    print(f"Server is running at http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT)
    