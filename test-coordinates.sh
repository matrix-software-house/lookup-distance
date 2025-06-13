#!/bin/bash

# Italian Cities Coordinate Testing for Distance Lookup Service
# Usage: ./test-coordinates.sh

BASE_URL="https://distance.lookupferrara.it"

echo "🇮🇹 Testing Italian Cities with Coordinates"
echo "==========================================="

# Italian cities coordinates
declare -A cities=(
    ["Roma"]="41.9028,12.4964"
    ["Milano"]="45.4642,9.1900"
    ["Napoli"]="40.8518,14.2681"
    ["Torino"]="45.0703,7.6869"
    ["Palermo"]="38.1157,13.3615"
    ["Genova"]="44.4056,8.9463"
    ["Bologna"]="44.4949,11.3426"
    ["Firenze"]="43.7696,11.2558"
    ["Bari"]="41.1171,16.8719"
    ["Catania"]="37.5079,15.0830"
    ["Venezia"]="45.4408,12.3155"
    ["Verona"]="45.4384,10.9916"
    ["Messina"]="38.1938,15.5540"
    ["Padova"]="45.4064,11.8768"
    ["Trieste"]="45.6495,13.7768"
    ["Brescia"]="45.5416,10.2118"
    ["Taranto"]="40.4668,17.2725"
    ["Prato"]="43.8777,11.1023"
    ["Reggio_Calabria"]="38.1109,15.6617"
    ["Modena"]="44.6471,10.9252"
    ["Reggio_Emilia"]="44.6989,10.6297"
    ["Perugia"]="43.1122,12.3888"
    ["Livorno"]="43.5485,10.3106"
    ["Ravenna"]="44.4173,12.1965"
    ["Cagliari"]="39.2238,9.1217"
    ["Foggia"]="41.4621,15.5444"
    ["Rimini"]="44.0678,12.5695"
    ["Salerno"]="40.6824,14.7681"
    ["Ferrara"]="44.8378,11.6197"
    ["Sassari"]="40.7259,8.5540"
)

echo "📍 Available cities for testing:"
for city in "${!cities[@]}"; do
    echo "   $city: ${cities[$city]}"
done

echo ""
echo "🧪 Running test: Roma to Milano"
echo "==============================="

roma_coords="${cities[Roma]}"
milano_coords="${cities[Milano]}"

echo "📍 Roma coordinates: $roma_coords"
echo "📍 Milano coordinates: $milano_coords"
echo ""

# Test with coordinates
echo "🔄 Testing with coordinates..."
response=$(curl -s "$BASE_URL/distance?origin=$roma_coords&destination=$milano_coords")
echo "📊 Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "🧪 Running test: Ferrara to Bologna"
echo "===================================="

ferrara_coords="${cities[Ferrara]}"
bologna_coords="${cities[Bologna]}"

echo "📍 Ferrara coordinates: $ferrara_coords"
echo "📍 Bologna coordinates: $bologna_coords"
echo ""

# Test with coordinates
echo "🔄 Testing with coordinates..."
response=$(curl -s "$BASE_URL/distance?origin=$ferrara_coords&destination=$bologna_coords")
echo "📊 Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

echo ""
echo "💡 Usage Examples:"
echo "=================="
echo "# Test any two cities:"
echo "curl \"$BASE_URL/distance?origin=\${cities[Roma]}&destination=\${cities[Milano]}\""
echo ""
echo "# Mix coordinates with addresses:"
echo "curl \"$BASE_URL/distance?origin=44.8378,11.6197&destination=Bologna,+Italy\""
echo ""
echo "# Use specific addresses:"
echo "curl \"$BASE_URL/distance?origin=Piazza+San+Marco,+Venezia&destination=Colosseo,+Roma\""
