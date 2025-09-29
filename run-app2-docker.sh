#!/bin/bash

# Script per avviare app2 con volumi Docker condivisi
# Il file points_of_interest.json sarà accessibile in ~/lookup-fe-distance2/

echo "🚀 Avvio Docker per app2 con volumi condivisi"
echo "============================================="

# Crea la cartella condivisa se non esiste
echo "📁 Creazione cartella condivisa..."
mkdir -p ~/lookup-fe-distance2

# Ferma eventuali container precedenti
echo "🛑 Ferma container precedenti..."
docker stop lookup-distance-service-app2 2>/dev/null || true
docker rm lookup-distance-service-app2 2>/dev/null || true

# Avvia con docker-compose
echo "🏗️  Building e avvio con docker-compose..."
docker-compose -f docker-compose.app2.yml up --build -d

echo ""
echo "✅ Container avviato!"
echo ""
echo "📁 File condivisi in: ~/lookup-fe-distance2/"
echo "   - points_of_interest.json (punti di interesse)"
echo "   - distance_cache.json (cache distanze)"
echo ""
echo "🌐 Endpoints disponibili:"
echo "   - http://localhost:5002/get_points?secret=your_secret"
echo "   - http://localhost:5002/distance?origin=lat,lon&destination=lat,lon"
echo "   - http://localhost:5002/all_distances?origin=lat,lon"
echo ""
echo "📊 Monitoraggio:"
echo "   docker logs -f lookup-distance-service-app2"
echo "   ./test-app2.sh"
echo ""
echo "🔍 File condivisi:"
echo "   ls -la ~/lookup-fe-distance2/"