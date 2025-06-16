# app.py
from flask import Flask, request, jsonify, send_file, make_response
import requests
import os
from dotenv import load_dotenv
# CORS moved to Nginx configuration

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PORT = 5001
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.before_request
def log_request():
    print(f"Received {request.method} request for {request.path}")


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


@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    # if request.method == 'OPTIONS':
    #     response = make_response()
    #     response.headers['Access-Control-Allow-Origin']  = 'http://localhost:5173'
    #     response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    #     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    #     return response

    if 'audio' not in request.files:
        return 'No audio file provided', 400

    print("Received audio file")
    audio_file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, 'latest_audio.webm')
    audio_file.save(file_path)

    response = make_response(send_file(file_path, mimetype='audio/webm'))
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    # print(response)
    return response



# Start the Flask server
if __name__ == '__main__':
    print(f"Server is running at http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT)
    