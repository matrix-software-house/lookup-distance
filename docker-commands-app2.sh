#!/bin/bash

# Comandi Docker run manuali per app2
# Questi comandi ti permettono di eseguire il container con maggiore controllo

echo "🐳 Comandi Docker per app2 con volumi condivisi"
echo "==============================================="
echo ""

# Crea la directory se non esiste
mkdir -p ~/lookup-fe-distance2

echo "1️⃣  Build dell'immagine:"
echo "docker build -f Dockerfile2 -t lookup-distance-app2 ."
echo ""

echo "2️⃣  Run con volumi condivisi (raccomandato):"
cat << 'EOF'
docker run -d \
  --name lookup-distance-service-app2 \
  -p 5002:5002 \
  --env-file .env \
  -v ~/lookup-fe-distance2:/app/shared \
  --restart unless-stopped \
  lookup-distance-app2
EOF
echo ""

echo "3️⃣  Run con singoli file montati:"
cat << 'EOF'
docker run -d \
  --name lookup-distance-service-app2 \
  -p 5002:5002 \
  --env-file .env \
  -v ~/lookup-fe-distance2/points_of_interest.json:/app/points_of_interest.json \
  -v ~/lookup-fe-distance2/distance_cache.json:/app/distance_cache.json \
  --restart unless-stopped \
  lookup-distance-app2
EOF
echo ""

echo "4️⃣  Run in modalità development (con logs visibili):"
cat << 'EOF'
docker run --rm \
  --name lookup-distance-service-app2 \
  -p 5002:5002 \
  --env-file .env \
  -v ~/lookup-fe-distance2:/app/shared \
  -v $(pwd):/app \
  lookup-distance-app2
EOF
echo ""

echo "📁 I file saranno salvati in:"
echo "   ~/lookup-fe-distance2/points_of_interest.json"
echo "   ~/lookup-fe-distance2/distance_cache.json"
echo ""

echo "🔧 Comandi di utilità:"
echo "   docker logs -f lookup-distance-service-app2  # Visualizza logs"
echo "   docker stop lookup-distance-service-app2     # Ferma container"
echo "   docker start lookup-distance-service-app2    # Riavvia container"
echo "   ls -la ~/lookup-fe-distance2/                # Lista file condivisi"