# Distance API v2 - Manual

**Base URL:** `https://distance2.lookupferrara.it`

This API provides walking distance calculations between user locations and predefined points of interest (POIs) in Ferrara, Italy. The service uses anti-abuse mechanisms and caching to optimize performance while preventing API misuse.

## 🔑 Authentication

Some endpoints require authentication using a secret parameter to prevent abuse.

## 📍 Endpoints

### 1. Get Points of Interest

**Endpoint:** `GET /get_points`

Retrieves and refreshes the list of points of interest from the Strapi CMS.

**Parameters:**
- `secret` (required): Admin secret for authentication

**Example:**
```bash
curl "https://distance2.lookupferrara.it/get_points?secret=YOUR_SECRET_HERE"
```

**Response:**
```json
{
  "success": true,
  "points_loaded": 11,
  "points": [
    {
      "id": 86,
      "lat": 44.826410189178596,
      "lon": 11.630261171165124,
      "name": "Porta Romana"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `401`: Invalid or missing secret
- `500`: Error fetching from Strapi

---

### 2. Calculate Distance

**Endpoint:** `GET /distance`

Calculates walking distance and duration between an origin point and a specific point of interest.

**Parameters:**
- `origin` (required): Origin coordinates in format `latitude,longitude`
- `destination` (required): Destination coordinates in format `latitude,longitude`

**Example:**
```bash
curl "https://distance2.lookupferrara.it/distance?origin=44.8220125,11.6275&destination=44.8261762,11.6220539"
```

**Response (Close Distance):**
```json
{
  "distance": 967,
  "duration": 782,
  "id": 94
}
```

distance is in meters.
duration is in seconds

**Response (Far Distance):**
```json
{
  "more_than": 200
}
```

integer value is in km

**Response (Invalid Destination):**
```json
{
  "error": "Invalid destination point"
}
```

**Field Descriptions:**
- `distance`: Walking distance in meters
- `duration`: Walking time in seconds
- `id`: Point of interest ID
- `more_than`: Distance threshold in kilometers when too far

**Status Codes:**
- `200`: Success
- `400`: Missing or invalid parameters
- `429`: Rate limit exceeded
- `500`: Server error

---

### 3. Calculate All Distances

**Endpoint:** `GET /all_distances`

Calculates distances from an origin point to all available points of interest.

**Parameters:**
- `origin` (required): Origin coordinates in format `latitude,longitude`

**Example:**
```bash
curl "https://distance2.lookupferrara.it/all_distances?origin=44.8220125,11.6275"
```

**Response:**
```json
[
  {
    "distance": 568,
    "duration": 470,
    "id": 86
  },
  {
    "distance": 1805,
    "duration": 1479,
    "id": 87
  },
  {
    "more_than": 10,
    "id": 92
  }
]
```

**Status Codes:**
- `200`: Success
- `400`: Missing origin parameter
- `429`: Rate limit exceeded
- `500`: Server error

---

## 📊 Rate Limiting

The API implements rate limiting to prevent abuse:

- **Global limits:** 500 requests/day, 100 requests/hour, 20 requests/minute
- **Per-endpoint limits:** Some endpoints have additional restrictions
- **Rate limit headers:** Check response headers for current limits

When rate limited, you'll receive a `429` status code with retry information.

## 🗺️ Coordinate Format

All coordinates must be provided in decimal degrees format:
- **Format:** `latitude,longitude`
- **Example:** `44.8220125,11.6275`
- **Precision:** Up to 6 decimal places

## 📏 Distance Calculations

### Close Distances (≤ 10km)
- Uses Google Maps Walking API or OpenRouteService
- Returns exact distance in meters and duration in seconds
- Results are cached for performance

### Far Distances (> 10km)
- Uses Haversine formula for quick calculation
- Returns stepped thresholds: `{"more_than": 10}`, `{"more_than": 20}`, etc.
- Thresholds increase in 10km steps

## 🏛️ Points of Interest

The API serves historical and cultural points of interest in Ferrara, Italy, including:

- **Porta Romana** (ID: 86) - Historical city gate
- **Piazza del Travaglio** (ID: 87) - UNESCO World Heritage square
- **Porta Paola** (ID: 92) - Monumental entrance gate
- **Baluardo di Sant'Antonio** (ID: 94) - Renaissance bastion
- **Casa dell'Ortolano** (ID: 97) - Historic rural court
- **Palazzo Tassoni** (ID: 99) - Renaissance palace
- **Basilica di San Giorgio** (ID: 101) - Ancient basilica
- **Bagni Ducali** (ID: 102) - Renaissance residence
- **Centro Slavich** (ID: 103) - Cultural center
- **Baluardo dell'Amore** (ID: 104) - Archaeological park
- **Baluardo di San Pietro** (ID: 105) - Entrance bastion

## 🚦 Error Handling

### Common Error Responses

**Invalid Parameters:**
```json
{
  "error": "You must provide both origin and destination coordinates"
}
```

**Invalid Destination:**
```json
{
  "error": "Invalid destination point"
}
```

**Rate Limited:**
```json
{
  "error": "Too many requests. Please wait before making another request.",
  "retry_after": 60
}
```

**Server Error:**
```json
{
  "error": "Error while accessing external API"
}
```

## 🔧 Integration Examples

### JavaScript/Fetch
```javascript
async function getDistance(originLat, originLon, destLat, destLon) {
  const response = await fetch(
    `https://distance2.lookupferrara.it/distance?origin=${originLat},${originLon}&destination=${destLat},${destLon}`
  );
  return await response.json();
}
```

### Python/Requests
```python
import requests

def get_all_distances(origin_lat, origin_lon):
    url = f"https://distance2.lookupferrara.it/all_distances"
    params = {"origin": f"{origin_lat},{origin_lon}"}
    response = requests.get(url, params=params)
    return response.json()
```

### cURL
```bash
# Get distances to all POIs
curl "https://distance2.lookupferrara.it/all_distances?origin=44.8220125,11.6275"

# Get specific distance
curl "https://distance2.lookupferrara.it/distance?origin=44.8220125,11.6275&destination=44.8261762,11.6220539"
```

## 📝 Notes

- The service prioritizes performance through intelligent caching
- Coordinates are automatically rounded to 4 decimal places for cache efficiency
- Only valid POI coordinates are accepted as destinations
- The API is optimized for the Ferrara city area
- All distances are calculated for walking routes
- Response times are typically under 100ms for cached results

## 🆘 Support

For technical support or to report issues, please contact the development team or check the API status at the base URL.

---

*Last updated: September 2025*