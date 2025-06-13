


# 🗺️ Distance Lookup Service

A Flask-based web service that provides walking distance calculations between two locations using the Google Distance Matrix API.

## 🚀 Features

- Get walking distances between any two locations worldwide
- RESTful API with JSON responses
- Docker containerization for easy deployment
- CORS support for web applications
- Error handling for invalid requests
- Health checks and monitoring

## 📦 Requirements

- Docker and Docker Compose
- Google Maps API Key (Distance Matrix API enabled)

## 🛠️ Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/iwan/dev/python/lookup_distance
   ```

2. **Set up your Google API Key:**
   Create a `.env` file in the project root:
   ```bash
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

3. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```

   The service will be available at `http://localhost:5001`

## 🧪 Testing Your Service

### Method 1: Command Line with curl

**Basic test:**
```bash
curl "http://localhost:5001/distance?origin=New+York,NY&destination=Boston,MA"
```

**Pretty printed JSON:**
```bash
curl -s "http://localhost:5001/distance?origin=New+York,NY&destination=Boston,MA" | python3 -m json.tool
```

**Quick test script:**
```bash
./quick_test.sh
./quick_test.sh "London, UK" "Paris, France"
```

### Method 2: Python Test Suite

Run the comprehensive test suite:
```bash
python3 test_service.py
```

This will test:
- ✅ Basic distance lookup
- ✅ Error handling (missing parameters)
- ✅ International locations
- ✅ Invalid location handling
- ✅ Service health check

### Method 3: Web Interface

Open `test.html` in your browser for a user-friendly testing interface:
```bash
open test.html
```

Features:
- Interactive form for testing locations
- Quick example buttons
- Real-time results display
- Error handling

### Method 4: Postman Collection

Import `Distance_Lookup_Service.postman_collection.json` into Postman for API testing with pre-configured requests.

### Method 5: Browser Direct Testing

Navigate to these URLs in your browser:

- **Basic test:** http://localhost:5001/distance?origin=New%20York,%20NY&destination=Boston,%20MA
- **International:** http://localhost:5001/distance?origin=London,%20UK&destination=Paris,%20France
- **Error test:** http://localhost:5001/distance?origin=New%20York,%20NY (missing destination)

## 📖 API Documentation

### Endpoint: GET /distance

**Parameters:**
- `origin` (required): Starting location (string)
- `destination` (required): Ending location (string)

**Example Request:**
```bash
GET /distance?origin=New York, NY&destination=Boston, MA
```

**Example Response:**
```json
{
  "destination_addresses": ["Boston, MA, USA"],
  "origin_addresses": ["New York, NY, USA"],
  "rows": [{
    "elements": [{
      "distance": {
        "text": "345 km",
        "value": 345197
      },
      "duration": {
        "text": "3 days 8 hours",
        "value": 287055
      },
      "status": "OK"
    }]
  }],
  "status": "OK"
}
```

**Error Response (400):**
```json
{
  "error": "You must provide both origin and destination locations."
}
```

**Error Response (500):**
```json
{
  "error": "Error while accessing Google API."
}
```

## 🐳 Docker Commands

**Start the service:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the service:**
```bash
docker-compose down
```

**Rebuild and restart:**
```bash
docker-compose up --build
```

**Check container status:**
```bash
docker-compose ps
```

## 🔧 Development

**Run locally without Docker:**
```bash
pip install -r requirements.txt
python app.py
```

**Run tests:**
```bash
python3 test_service.py
```

## 📝 Example Use Cases

### 1. City-to-City Distances
```bash
curl "http://localhost:5001/distance?origin=San+Francisco,CA&destination=Los+Angeles,CA"
```

### 2. International Routes
```bash
curl "http://localhost:5001/distance?origin=Tokyo,Japan&destination=Osaka,Japan"
```

### 3. Address-to-Address
```bash
curl "http://localhost:5001/distance?origin=1600+Amphitheatre+Parkway,+Mountain+View,+CA&destination=1+Hacker+Way,+Menlo+Park,+CA"
```

## ⚠️ Important Notes

- The service returns **walking distances** by default
- All distances are calculated using Google's Distance Matrix API
- Rate limits apply based on your Google API quota
- Invalid locations will return appropriate error responses
- The service includes CORS headers for web application integration

## 🛡️ Security

- The service runs as a non-root user in Docker
- Environment variables are used for sensitive configuration
- No sensitive data is logged or exposed

## 🔍 Troubleshooting

**Service not responding:**
```bash
# Check if container is running
docker-compose ps

# Check logs
docker-compose logs lookup-distance-api
```

**API key issues:**
- Ensure your Google API key is valid
- Enable the Distance Matrix API in Google Cloud Console
- Check your API quotas and billing

**CORS issues:**
- The service includes CORS headers
- For production, consider configuring specific origins

## 📊 Monitoring

The service includes health checks:
- Docker health check every 30 seconds
- Automatic restart on failure
- Logs accessible via `docker-compose logs`

---

🎉 **Your Flask Distance Lookup Service is ready to use!**

