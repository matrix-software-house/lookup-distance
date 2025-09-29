#!/bin/bash

# Script per monitorare richieste sospette alla API
# Usage: ./monitor-requests.sh

BASE_URL="http://localhost:5001"

echo "🔍 Rate Limiting & Request Monitor"
echo "=================================="

echo ""
echo "📊 Current API Statistics:"
curl -s "$BASE_URL/admin/stats" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'Active IPs: {data[\"active_ips\"]}')
    print(f'Rate limit: {data[\"rate_limit_settings\"][\"max_requests\"]} requests per {data[\"rate_limit_settings\"][\"window_seconds\"]} seconds')
    print('')
    print('IP Statistics:')
    for ip, stats in data['ip_stats'].items():
        status = '🚨 RATE LIMITED' if stats['is_rate_limited'] else '✅ OK'
        print(f'  {ip}: {stats[\"recent_requests\"]} recent requests {status}')
except:
    print('Error parsing JSON response')
"

echo ""
echo "🧪 Testing rate limiting..."
echo "Making 12 rapid requests to trigger rate limiting:"

for i in {1..12}; do
    echo -n "Request $i: "
    response=$(curl -s -w "%{http_code}" "$BASE_URL/distance?origin=44.8378,11.6197&destination=44.4949,11.3426")
    http_code="${response: -3}"
    
    if [ "$http_code" = "429" ]; then
        echo "🚨 Rate limited (HTTP 429)"
    elif [ "$http_code" = "200" ]; then
        echo "✅ OK (HTTP 200)"
    else
        echo "❓ HTTP $http_code"
    fi
    
    sleep 0.5
done

echo ""
echo "📊 Updated Statistics:"
curl -s "$BASE_URL/admin/stats" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'Active IPs: {data[\"active_ips\"]}')
    for ip, stats in data['ip_stats'].items():
        status = '🚨 RATE LIMITED' if stats['is_rate_limited'] else '✅ OK'
        print(f'  {ip}: {stats[\"recent_requests\"]} recent requests {status}')
except:
    print('Error parsing JSON response')
"

echo ""
echo "💡 Tips:"
echo "- Rate limiting è attivo a livello Flask (Flask-Limiter)"
echo "- Rate limiting personalizzato: 10 richieste per minuto per IP"
echo "- Attività sospette vengono loggdate nella console"
echo "- Usa /admin/stats per monitorare in tempo reale"