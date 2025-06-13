#!/bin/zsh

# Quick test script for Distance Lookup Service
# Usage: ./quick_test.sh [origin] [destination]

set -e

BASE_URL="http://localhost:5001"
ORIGIN="${1:-New York, NY}"
DESTINATION="${2:-Boston, MA}"

echo "🧪 Testing Distance Lookup Service"
echo "=================================="
echo "Origin: $ORIGIN"
echo "Destination: $DESTINATION"
echo ""

# URL encode spaces and special characters
ENCODED_ORIGIN=$(echo "$ORIGIN" | sed 's/ /+/g')
ENCODED_DESTINATION=$(echo "$DESTINATION" | sed 's/ /+/g')

# Test the service
echo "📡 Making request..."
RESPONSE=$(curl -s "$BASE_URL/distance?origin=$ENCODED_ORIGIN&destination=$ENCODED_DESTINATION")

# Check if curl was successful
if [ $? -eq 0 ]; then
    echo "✅ Request successful!"
    echo ""
    echo "📊 Response:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
    echo "❌ Request failed!"
    exit 1
fi
