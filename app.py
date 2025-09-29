# app.py
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from math import radians, cos, sin, sqrt, atan2
import time
from collections import defaultdict, deque

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour", "10 per minute"]
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTE_API_KEY = os.getenv("OPENROUTE_API_KEY")
CENTER = os.getenv("CENTER")

PORT = 5001
CENTER = tuple(map(float, CENTER.split(",")))  # Convert to tuple of floats
MAX_DIST = 10 # Maximum allowed distance from center in km

# Rate limiting storage
request_history = defaultdict(deque)
RATE_LIMIT_WINDOW = 60  # 60 secondi
RATE_LIMIT_MAX_REQUESTS = 10  # max 10 richieste per minuto per IP

def is_rate_limited(ip_address):
    """Verifica se un IP ha superato il limite di richieste"""
    current_time = time.time()
    
    # Pulisce le richieste vecchie (fuori dalla finestra temporale)
    while request_history[ip_address] and current_time - request_history[ip_address][0] > RATE_LIMIT_WINDOW:
        request_history[ip_address].popleft()
    
    # Verifica se ha superato il limite
    if len(request_history[ip_address]) >= RATE_LIMIT_MAX_REQUESTS:
        return True
    
    # Aggiunge la richiesta corrente
    request_history[ip_address].append(current_time)
    return False

def log_suspicious_activity(ip_address, request_count):
    """Log delle attività sospette"""
    print(f"⚠️  SUSPICIOUS ACTIVITY: IP {ip_address} made {request_count} requests in {RATE_LIMIT_WINDOW} seconds")
    # Qui potresti aggiungere logging su file o invio di notifiche

@app.route('/distance', methods=['GET'])
@limiter.limit("5 per minute")  # Limite specifico per questo endpoint
def get_distance():
    # Ottieni l'IP del client (considera proxy/load balancer)
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
    
    # Verifica rate limiting personalizzato
    if is_rate_limited(client_ip):
        log_suspicious_activity(client_ip, len(request_history[client_ip]))
        return jsonify({
            "error": "Too many requests. Please wait before making another request.",
            "retry_after": RATE_LIMIT_WINDOW
        }), 429

    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # Check if both origin and destination are provided
    if not origin or not destination:
        return jsonify({ "error": "You must provide both origin and destination locations." }), 400

    # origin is in "lat,lon" format
    d1 = calc_distance(list(map(float, origin.split(','))))  # split and convert to float
    d2 = calc_distance(list(map(float, destination.split(','))))
    print(f"Calculated distances from center: origin={d1} km, destination={d2} km")

    if d1 > MAX_DIST or d2 > MAX_DIST:
        print("AAAAA")
        return jsonify({ "error": f"You are too far away." }), 400

    if os.getenv("SELECTOR") == "openroute":
        return get_distance_with_openroute(list(map(float, origin.split(','))), list(map(float, destination.split(','))))
    else:
        return get_distance_with_google_maps(origin, destination)
    


def get_distance_with_google_maps(origin, destination):
    """Get distance using Google Maps API"""
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={requests.utils.quote(origin)}"
        f"&destinations={requests.utils.quote(destination)}"
        f"&key={GOOGLE_API_KEY}&mode=walking"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        map = response.json()
        distance = map['rows'][0]['elements'][0]['distance']['value']
        duration = map['rows'][0]['elements'][0]['duration']['value']
        return jsonify({'distance': distance, 'duration': duration}), 200
    except requests.RequestException:
        return jsonify({ "error": "Error while accessing Google API." }), 500


def get_distance_with_openroute(origin, destination):
    """Get distance using OpenRouteService API"""
    url = "https://api.openrouteservice.org/v2/directions/foot-walking"
    headers = {
        "Authorization": OPENROUTE_API_KEY,
        "Content-Type": "application/json"
    }
    params = {
        "start": f"{origin[1]},{origin[0]}",
        "end": f"{destination[1]},{destination[0]}"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        map = response.json()
        print(map)
        return jsonify(map['features'][0]['properties']['summary']), 200
        
        # return map['features'][0]['properties']['summary']
    except requests.RequestException:
        return jsonify({ "error": "Error while accessing OpenRouteService API." }), 500


def calc_distance(point1, point2=CENTER):

    # Haversine formula to calculate the distance between two points on the Earth
    R = 6371.0  # Radius of the Earth in kilometers

    lat1, lon1 = point1
    lat2, lon2 = point2

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

@app.route('/admin/stats', methods=['GET'])
@limiter.limit("10 per minute")
def get_stats():
    """Endpoint per monitorare le statistiche delle richieste"""
    current_time = time.time()
    stats = {}
    
    for ip, requests_deque in request_history.items():
        # Conta solo le richieste recenti
        recent_requests = sum(1 for req_time in requests_deque 
                            if current_time - req_time <= RATE_LIMIT_WINDOW)
        if recent_requests > 0:
            stats[ip] = {
                "recent_requests": recent_requests,
                "total_requests": len(requests_deque),
                "is_rate_limited": recent_requests >= RATE_LIMIT_MAX_REQUESTS
            }
    
    return jsonify({
        "active_ips": len(stats),
        "rate_limit_settings": {
            "window_seconds": RATE_LIMIT_WINDOW,
            "max_requests": RATE_LIMIT_MAX_REQUESTS
        },
        "ip_stats": stats
    })



# Start the Flask server
if __name__ == '__main__':
    print(f"Server is running at http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT)


# 44.837622, 11.611486