# 📍 Coordinate Usage Guide for Distance Lookup Service

## 🌍 **How to Use Coordinates**

Your service at `https://distance.lookupferrara.it` supports coordinates in multiple formats:

### **1. Pure Coordinates (Latitude,Longitude)**
```bash
# Format: latitude,longitude (no spaces, comma separated)
curl "https://distance.lookupferrara.it/distance?origin=41.9028,12.4964&destination=45.4642,9.1900"
```

### **2. Mixed Format (Coordinates + Address)**
```bash
# Coordinates to address
curl "https://distance.lookupferrara.it/distance?origin=44.8378,11.6197&destination=Bologna,+Italy"

# Address to coordinates  
curl "https://distance.lookupferrara.it/distance?origin=Ferrara,+Italy&destination=44.4949,11.3426"
```

### **3. Specific Addresses with Coordinates**
```bash
# Very precise locations
curl "https://distance.lookupferrara.it/distance?origin=44.8378,11.6197&destination=Piazza+Maggiore,+Bologna"
```

## 🇮🇹 **Major Italian Cities Coordinates**

| City | Coordinates (Lat,Lng) | Example Usage |
|------|----------------------|---------------|
| **Roma** | `41.9028,12.4964` | `origin=41.9028,12.4964` |
| **Milano** | `45.4642,9.1900` | `origin=45.4642,9.1900` |
| **Napoli** | `40.8518,14.2681` | `origin=40.8518,14.2681` |
| **Torino** | `45.0703,7.6869` | `origin=45.0703,7.6869` |
| **Firenze** | `43.7696,11.2558` | `origin=43.7696,11.2558` |
| **Bologna** | `44.4949,11.3426` | `origin=44.4949,11.3426` |
| **Venezia** | `45.4408,12.3155` | `origin=45.4408,12.3155` |
| **Genova** | `44.4056,8.9463` | `origin=44.4056,8.9463` |
| **Palermo** | `38.1157,13.3615` | `origin=38.1157,13.3615` |
| **Bari** | `41.1171,16.8719` | `origin=41.1171,16.8719` |
| **Ferrara** | `44.8378,11.6197` | `origin=44.8378,11.6197` |

## 🧪 **Test Examples**

### **Quick Tests:**
```bash
# Rome to Milan
curl "https://distance.lookupferrara.it/distance?origin=41.9028,12.4964&destination=45.4642,9.1900"

# Ferrara to Bologna  
curl "https://distance.lookupferrara.it/distance?origin=44.8378,11.6197&destination=44.4949,11.3426"

# Naples to Palermo
curl "https://distance.lookupferrara.it/distance?origin=40.8518,14.2681&destination=38.1157,13.3615"

# Venice to Florence
curl "https://distance.lookupferrara.it/distance?origin=45.4408,12.3155&destination=43.7696,11.2558"
```

### **Mixed Format Examples:**
```bash
# Coordinates to city name
curl "https://distance.lookupferrara.it/distance?origin=44.8378,11.6197&destination=Bologna,+Italy"

# Specific location to coordinates
curl "https://distance.lookupferrara.it/distance?origin=Stazione+Centrale,+Milano&destination=41.9028,12.4964"

# Address to precise coordinates
curl "https://distance.lookupferrara.it/distance?origin=Piazza+San+Marco,+Venezia&destination=43.7696,11.2558"
```

## 📋 **Response Format**

The service returns the same format regardless of input type:

```json
{
  "destination_addresses": ["Resolved address"],
  "origin_addresses": ["Resolved address"], 
  "rows": [{
    "elements": [{
      "distance": {
        "text": "48.9 km",
        "value": 48867
      },
      "duration": {
        "text": "11 hours 6 mins", 
        "value": 39984
      },
      "status": "OK"
    }]
  }],
  "status": "OK"
}
```

## 💡 **Pro Tips**

1. **Precision**: Use 4-6 decimal places for precise locations
2. **URL Encoding**: The service handles URL encoding automatically
3. **Mixed Formats**: You can mix coordinates and addresses freely
4. **Validation**: Google Maps API will resolve coordinates to nearest valid address
5. **Error Handling**: Invalid coordinates return appropriate error messages

## 🚀 **Advanced Usage**

### **Using the Test Script:**
```bash
# Run comprehensive coordinate tests
./test-coordinates.sh
```

### **For Web Applications:**
```javascript
// JavaScript example
const origin = "44.8378,11.6197"; // Ferrara coordinates
const destination = "Bologna, Italy";
const url = `https://distance.lookupferrara.it/distance?origin=${origin}&destination=${encodeURIComponent(destination)}`;

fetch(url)
  .then(response => response.json())
  .then(data => console.log(data));
```

### **For Mobile Apps:**
```bash
# Get user's current location coordinates and calculate distance
curl "https://distance.lookupferrara.it/distance?origin=USER_LAT,USER_LNG&destination=DEST_LAT,DEST_LNG"
```

---

🎯 **Your service now supports all coordinate formats and is ready for production use!**
