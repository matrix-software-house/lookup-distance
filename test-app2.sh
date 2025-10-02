#!/bin/bash

# Test script per app2.py - Distance Lookup Service v2 (Anti-Abuse)
# Usage: ./test-app2.sh

BASE_URL="http://localhost:5002"
ADMIN_SECRET="abcd1234"

echo "🧪 Testing Distance Lookup Service v2 (Anti-Abuse)"
echo "================================================="

echo ""
echo "0️⃣  Testing Health Check endpoints"
echo "----------------------------------"
echo "Root endpoint:"
curl -s "$BASE_URL/" | python3 -m json.tool 2>/dev/null || curl -s "$BASE_URL/"

echo ""
echo "Health endpoint:"
curl -s "$BASE_URL/health" | python3 -m json.tool 2>/dev/null || curl -s "$BASE_URL/health"

echo ""
echo "Health check via distance endpoint:"
curl -s "$BASE_URL/distance?origin=test&destination=test" | python3 -m json.tool 2>/dev/null || curl -s "$BASE_URL/distance?origin=test&destination=test"

echo ""
echo "1️⃣  Testing /get_points endpoint (loading points from Strapi)"
echo "-----------------------------------------------------------"
response=$(curl -s "$BASE_URL/get_points?secret=$ADMIN_SECRET")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "2️⃣  Testing /admin/stats endpoint"
echo "--------------------------------"
response=$(curl -s "$BASE_URL/admin/stats")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "3️⃣  Testing /distance endpoint (valid point)"
echo "-------------------------------------------"
# Usa coordinate di esempio - dovrai aggiornare con veri punti dal tuo Strapi
echo "Testing with sample coordinates (update with real points from your Strapi)"
response=$(curl -s "$BASE_URL/distance?origin=45.188642,9.145117&destination=45.196458,9.148310")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "4️⃣  Testing /distance endpoint (invalid point)"
echo "----------------------------------------------"
response=$(curl -s "$BASE_URL/distance?origin=45.188642,9.145117&destination=99.999999,99.999999")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "5️⃣  Testing /distance endpoint (too far away)"
echo "--------------------------------------------"
# Roma -> Milano (dovrebbe essere > 10km)
response=$(curl -s "$BASE_URL/distance?origin=41.9028,12.4964&destination=45.4642,9.1900")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "6️⃣  Testing /all_distances endpoint"
echo "----------------------------------"
response=$(curl -s "$BASE_URL/all_distances?origin=45.188642,9.145117")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "7️⃣  Testing rate limiting (10 rapid requests)"
echo "--------------------------------------------"
for i in {1..10}; do
    echo -n "Request $i: "
    response=$(curl -s -w "%{http_code}" "$BASE_URL/distance?origin=45.188642,9.145117&destination=45.196458,9.148310")
    http_code="${response: -3}"
    
    if [ "$http_code" = "429" ]; then
        echo "🚨 Rate limited (HTTP 429)"
    elif [ "$http_code" = "200" ]; then
        echo "✅ OK (HTTP 200)"
    else
        echo "❓ HTTP $http_code"
    fi
    
    sleep 0.2
done

echo ""
echo "8️⃣  Testing cache clearing"
echo "-------------------------"
response=$(curl -s -X POST "$BASE_URL/admin/cache/clear?secret=$ADMIN_SECRET")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "9️⃣  Final stats check"
echo "-------------------"
response=$(curl -s "$BASE_URL/admin/stats")
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "💡 Testing Tips:"
echo "==============="
echo "- Start the server: python app2.py"
echo "- Make sure your Strapi service is running at https://strapi2.lookupferrara.it"
echo "- Update STRAPI_BEARER_TOKEN in .env if needed"
echo "- Check points_of_interest.json and distance_cache.json files"
echo "- Use /get_points?secret=$ADMIN_SECRET to reload points from Strapi"
echo "- Cache is persistent across server restarts"
echo "- Rate limiting: 20 requests per minute per IP"