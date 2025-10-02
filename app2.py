# app2.py - Versione anti-abuso con punti di interesse predefiniti
from flask import Flask, request, jsonify
import requests
import os
import json
from dotenv import load_dotenv
# from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from math import radians, cos, sin, sqrt, atan2
import time
from collections import defaultdict, deque

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# CORS(app)

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour", "20 per minute"]
)

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTE_API_KEY = os.getenv("OPENROUTE_API_KEY") 
STRAPI_BEARER_TOKEN = os.getenv("STRAPI_BEARER_TOKEN", "abc123")
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "abcd1234")
PORT = 5002

# File paths for persistence - usa cartella condivisa se disponibile
SHARED_DIR = "/app/shared" if os.path.exists("/app/shared") else "./shared"

# Crea la cartella shared se non esiste
if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR, exist_ok=True)
    print(f"✅ Created directory: {SHARED_DIR}")

POINTS_FILE = os.path.join(SHARED_DIR, "points_of_interest.json")
CACHE_FILE = os.path.join(SHARED_DIR, "distance_cache.json")

# In-memory storage
points_of_interest = []
distance_cache = {}

# Rate limiting storage  
request_history = defaultdict(deque)
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX_REQUESTS = 20

def load_points_from_file():
    """Carica i punti di interesse dal file"""
    global points_of_interest
    try:
        with open(POINTS_FILE, 'r') as f:
            points_of_interest = json.load(f)
        print(f"✅ Loaded {len(points_of_interest)} points of interest from {POINTS_FILE}")
    except FileNotFoundError:
        print(f"⚠️  File {POINTS_FILE} not found, creating empty file")
        points_of_interest = []
        # Crea il file vuoto
        try:
            with open(POINTS_FILE, 'w') as f:
                json.dump([], f, indent=2)
            print(f"✅ Created empty points file: {POINTS_FILE}")
        except Exception as e:
            print(f"❌ Error creating points file: {e}")
    except Exception as e:
        print(f"❌ Error loading points from file: {e}")
        points_of_interest = []

def save_points_to_file():
    """Salva i punti di interesse nel file"""
    try:
        with open(POINTS_FILE, 'w') as f:
            json.dump(points_of_interest, f, indent=2)
        print(f"✅ Saved {len(points_of_interest)} points to {POINTS_FILE}")
    except Exception as e:
        print(f"❌ Error saving points to file: {e}")

def load_cache_from_file():
    """Carica la cache dal file"""
    global distance_cache
    try:
        with open(CACHE_FILE, 'r') as f:
            distance_cache = json.load(f)
        print(f"✅ Loaded {len(distance_cache)} cache entries from {CACHE_FILE}")
    except FileNotFoundError:
        print(f"⚠️  File {CACHE_FILE} not found, creating empty file")
        distance_cache = {}
        # Crea il file vuoto
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump({}, f, indent=2)
            print(f"✅ Created empty cache file: {CACHE_FILE}")
        except Exception as e:
            print(f"❌ Error creating cache file: {e}")
    except Exception as e:
        print(f"❌ Error loading cache from file: {e}")
        distance_cache = {}

def save_cache_to_file():
    """Salva la cache nel file"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(distance_cache, f, indent=2)
        print(f"✅ Saved {len(distance_cache)} cache entries to {CACHE_FILE}")
    except Exception as e:
        print(f"❌ Error saving cache to file: {e}")

def is_rate_limited(ip_address):
    """Verifica se un IP ha superato il limite di richieste"""
    current_time = time.time()
    
    # Pulisce le richieste vecchie
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

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcola la distanza usando la formula di Haversine (in metri)"""
    R = 6371000  # Raggio della Terra in metri
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return int(distance)  # Ritorna in metri come intero

def find_point_by_coordinates(lat, lon):
    """Trova un punto di interesse dalle sue coordinate"""
    for point in points_of_interest:
        if abs(point['lat'] - lat) < 0.0001 and abs(point['lon'] - lon) < 0.0001:
            return point
    return None

def round_coordinates(lat, lon, decimals=4):
    """Arrotonda le coordinate al numero specificato di decimali"""
    return round(lat, decimals), round(lon, decimals)

def get_cache_key(origin_lat, origin_lon, dest_lat, dest_lon):
    """Genera una chiave per la cache"""
    rounded_origin = round_coordinates(origin_lat, origin_lon)
    return f"{rounded_origin[0]},{rounded_origin[1]},{dest_lat},{dest_lon}"

def get_distance_with_google(origin_coords, dest_coords):
    """Ottiene distanza e durata usando Google Maps API"""
    origin_str = f"{origin_coords[0]},{origin_coords[1]}"
    dest_str = f"{dest_coords[0]},{dest_coords[1]}"
    
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={requests.utils.quote(origin_str)}"
        f"&destinations={requests.utils.quote(dest_str)}"
        f"&key={GOOGLE_API_KEY}&mode=walking"
    )
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        element = data['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance = element['distance']['value']  # in metri
            duration = element['duration']['value']   # in secondi
            return distance, duration
        else:
            return None, None
    except Exception as e:
        print(f"❌ Google API error: {e}")
        return None, None

def get_distance_with_openroute(origin_coords, dest_coords):
    """Ottiene distanza e durata usando OpenRouteService API"""
    # url = "https://api.openrouteservice.org/v2/directions/foot-walking"
    url = "https://ors.fabvision.it/ors/v2/directions/foot-walking"
    headers = {
        # "Authorization": OPENROUTE_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "coordinates": [[origin_coords[1], origin_coords[0]], [dest_coords[1], dest_coords[0]]]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        summary = result['routes'][0]['summary']
        distance = int(summary['distance'])  # in metri
        duration = int(summary['duration'])   # in secondi
        return distance, duration
    except Exception as e:
        print(f"❌ OpenRoute API error: {e}")
        return None, None

@app.route('/get_points', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def get_points():
    """Endpoint per ricaricare i punti di interesse da Strapi"""
    secret = request.args.get('secret')
    
    if secret != ADMIN_SECRET:
        return jsonify({"error": "Invalid secret"}), 401
    
    try:
        # Interroga Strapi
        headers = {"Authorization": f"Bearer {STRAPI_BEARER_TOKEN}"}
        response = requests.get("https://strapi2.lookupferrara.it/api/points", headers=headers, timeout=10)
        response.raise_for_status()
        
        strapi_data = response.json()

        print("------------")
        print(f"Received {len(strapi_data.get('data', []))} points from Strapi")
        print("------------")
        
        # Estrae i punti di interesse nel formato richiesto
        global points_of_interest
        points_of_interest = []
        
        for item in strapi_data.get('data', []):
            # I dati sono direttamente nell'item, non in 'attributes'
            points_of_interest.append({
                'id': item['id'],
                'lat': float(item.get('Latitude', 0)),
                'lon': float(item.get('Longitude', 0)),
                'name': item.get('Name', f"Point {item['id']}")  # Aggiungiamo anche il nome per debug
            })
        
        # Salva nel file
        save_points_to_file()
        
        return jsonify({
            "success": True,
            "points_loaded": len(points_of_interest),
            "points": points_of_interest
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to load points from Strapi: {str(e)}"}), 500

@app.route('/distance', methods=['GET'])
@limiter.limit("20 per minute")
def get_distance():
    """Endpoint per calcolare la distanza tra origin e destination"""
    # Rate limiting personalizzato
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
    
    if is_rate_limited(client_ip):
        log_suspicious_activity(client_ip, len(request_history[client_ip]))
        return jsonify({
            "error": "Too many requests. Please wait before making another request.",
            "retry_after": RATE_LIMIT_WINDOW
        }), 429
    
    # Parsing dei parametri
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        
        if not origin or not destination:
            return jsonify({"error": "Both origin and destination are required"}), 400
        
        # Health check endpoint
        if origin == "test" and destination == "test":
            return jsonify({
                "status": "healthy",
                "service": "Distance API v2",
                "timestamp": time.time(),
                "points_loaded": len(points_of_interest),
                "cache_entries": len(distance_cache),
                "message": "Service is running correctly"
            }), 200
        
        origin_lat, origin_lon = map(float, origin.split(','))
        dest_lat, dest_lon = map(float, destination.split(','))
        
    except ValueError:
        return jsonify({"error": "Invalid coordinate format. Use lat,lon"}), 400
    
    # Verifica che destination sia un punto valido
    dest_point = find_point_by_coordinates(dest_lat, dest_lon)
    if not dest_point:
        return jsonify({"error": "Invalid destination point"}), 400
    
    # Calcola distanza Haversine per controllo soglia
    haversine_dist = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    haversine_km = haversine_dist / 1000
    
    # Se troppo distante, ritorna step di 10km
    if haversine_km > 10:
        step = int((haversine_km // 10) * 10)
        if step < haversine_km:
            step += 10
        return jsonify({"more_than": step})
    
    # Controlla cache
    cache_key = get_cache_key(origin_lat, origin_lon, dest_lat, dest_lon)
    if cache_key in distance_cache:
        print(f"🎯 Cache hit for {cache_key}")
        cached_result = distance_cache[cache_key].copy()
        cached_result["id"] = dest_point['id']
        return jsonify(cached_result)
    
    # Cache miss - chiama API esterna
    print(f"🔄 Cache miss for {cache_key}, calling external API")
    
    # Prova prima Google, poi OpenRoute come fallback
    distance, duration = get_distance_with_google((origin_lat, origin_lon), (dest_lat, dest_lon))
    
    if distance is None:
        distance, duration = get_distance_with_openroute((origin_lat, origin_lon), (dest_lat, dest_lon))
    
    if distance is None:
        return jsonify({"error": "Unable to calculate distance"}), 500
    
    # Salva in cache
    result = {"distance": distance, "duration": duration}
    distance_cache[cache_key] = result
    save_cache_to_file()
    
    # Aggiungi ID e ritorna
    result["id"] = dest_point['id']
    return jsonify(result)

@app.route('/all_distances', methods=['GET'])
@limiter.limit("5 per minute")
def get_all_distances():
    """Endpoint per calcolare distanze da origin a tutti i punti di interesse"""
    # Rate limiting personalizzato
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
    
    if is_rate_limited(client_ip):
        log_suspicious_activity(client_ip, len(request_history[client_ip]))
        return jsonify({
            "error": "Too many requests. Please wait before making another request.",
            "retry_after": RATE_LIMIT_WINDOW
        }), 429
    
    # Parsing parametri
    try:
        origin = request.args.get('origin')
        if not origin:
            return jsonify({"error": "Origin is required"}), 400
        
        origin_lat, origin_lon = map(float, origin.split(','))
        
    except ValueError:
        return jsonify({"error": "Invalid coordinate format. Use lat,lon"}), 400
    
    results = []
    
    for point in points_of_interest:
        dest_lat, dest_lon = point['lat'], point['lon']
        
        # Calcola distanza Haversine per controllo soglia
        haversine_dist = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        haversine_km = haversine_dist / 1000
        
        # Se troppo distante
        if haversine_km > 10:
            step = int((haversine_km // 10) * 10)
            if step < haversine_km:
                step += 10
            results.append({"id": point['id'], "more_than": step})
            continue
        
        # Controlla cache
        cache_key = get_cache_key(origin_lat, origin_lon, dest_lat, dest_lon)
        if cache_key in distance_cache:
            cached_result = distance_cache[cache_key].copy()
            cached_result["id"] = point['id']
            results.append(cached_result)
            continue
        
        # Cache miss - calcola
        distance, duration = get_distance_with_google((origin_lat, origin_lon), (dest_lat, dest_lon))
        
        if distance is None:
            distance, duration = get_distance_with_openroute((origin_lat, origin_lon), (dest_lat, dest_lon))
        
        if distance is None:
            results.append({"id": point['id'], "error": "Unable to calculate distance"})
            continue
        
        # Salva in cache
        result = {"distance": distance, "duration": duration}
        distance_cache[cache_key] = result
        
        # Aggiungi alla risposta
        result["id"] = point['id']
        results.append(result)
    
    # Salva cache se è stata modificata
    save_cache_to_file()
    
    return jsonify(results)

@app.route('/admin/stats', methods=['GET'])
@limiter.limit("10 per minute")
def get_stats():
    """Endpoint per monitorare le statistiche"""
    current_time = time.time()
    stats = {}
    
    for ip, requests_deque in request_history.items():
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
        "points_of_interest_count": len(points_of_interest),
        "cache_entries": len(distance_cache),
        "rate_limit_settings": {
            "window_seconds": RATE_LIMIT_WINDOW,
            "max_requests": RATE_LIMIT_MAX_REQUESTS
        },
        "ip_stats": stats
    })

@app.route('/admin/cache/clear', methods=['POST'])
def clear_cache():
    """Endpoint per pulire la cache (richiede secret)"""
    secret = request.args.get('secret')
    if secret != ADMIN_SECRET:
        return jsonify({"error": "Invalid secret"}), 401
    
    global distance_cache
    cache_size = len(distance_cache)
    distance_cache = {}
    save_cache_to_file()
    
    return jsonify({"success": True, "cleared_entries": cache_size})

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint dedicato per health check"""
    return jsonify({
        "status": "healthy",
        "service": "Distance API v2",
        "version": "2.0",
        "timestamp": time.time(),
        "uptime": "service running",
        "points_loaded": len(points_of_interest),
        "cache_entries": len(distance_cache),
        "endpoints": [
            "/health",
            "/get_points",
            "/distance", 
            "/all_distances",
            "/admin/clear_cache"
        ],
        "message": "All systems operational"
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint con informazioni base"""
    return jsonify({
        "service": "Distance API v2",
        "version": "2.0",
        "description": "Walking distance calculation service for Ferrara POIs",
        "endpoints": {
            "health": "/health",
            "distance": "/distance?origin=lat,lon&destination=lat,lon",
            "all_distances": "/all_distances?origin=lat,lon",
            "get_points": "/get_points?secret=YOUR_SECRET"
        },
        "documentation": "See API_MANUAL.md for complete documentation"
    }), 200

# Carica dati all'avvio
load_points_from_file()
load_cache_from_file()

# Start the Flask server
if __name__ == '__main__':
    print(f"🚀 Distance Lookup Service v2 (Anti-Abuse)")
    print(f"📍 Loaded {len(points_of_interest)} points of interest")
    print(f"💾 Loaded {len(distance_cache)} cache entries")
    print(f"🌐 Server running at http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)