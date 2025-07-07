#!/bin/bash

# Docker Compose Troubleshooting Script for Distance Lookup Service
# Run this on your VPS to diagnose and fix Docker Compose issues

echo "🔧 Docker Compose Troubleshooting for Distance Lookup Service"
echo "============================================================="

# Check Docker version
echo "🐳 Checking Docker version..."
docker --version
echo ""

# Check Docker Compose version
echo "🐙 Checking Docker Compose version..."
if command -v docker-compose &> /dev/null; then
    docker-compose --version
else
    echo "❌ docker-compose not found, checking for docker compose plugin..."
    docker compose version 2>/dev/null || echo "❌ Docker Compose not installed"
fi
echo ""

# Check if Docker daemon is running
echo "🔄 Checking Docker daemon status..."
if systemctl is-active --quiet docker; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon is not running"
    echo "   Try: sudo systemctl start docker"
fi
echo ""

# Check available disk space
echo "💾 Checking disk space..."
df -h /
echo ""

# Check for old containers
echo "📦 Checking for existing containers..."
docker ps -a --filter name=lookup-distance
echo ""

# Check for existing images
echo "🖼️  Checking for existing images..."
docker images | grep lookup-distance
echo ""

# Clean up old containers and images
echo "🧹 Cleaning up old containers and images..."
echo "Stopping and removing old containers..."
docker stop $(docker ps -q --filter name=lookup-distance) 2>/dev/null || echo "No running containers to stop"
docker rm $(docker ps -aq --filter name=lookup-distance) 2>/dev/null || echo "No containers to remove"

echo "Removing old images..."
docker rmi $(docker images -q lookup-distance*) 2>/dev/null || echo "No images to remove"

echo "Pruning unused Docker resources..."
docker system prune -f

echo ""

# Check current directory and files
echo "📁 Checking current directory and files..."
pwd
ls -la
echo ""

# Check if required files exist
echo "📋 Checking required files..."
files=("app.py" "Dockerfile" "docker-compose.prod.yml" "requirements.txt" ".env")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Check .env file content (without showing sensitive data)
echo "🔑 Checking .env file..."
if [ -f ".env" ]; then
    if grep -q "GOOGLE_API_KEY" .env; then
        echo "✅ GOOGLE_API_KEY found in .env"
    else
        echo "❌ GOOGLE_API_KEY missing in .env"
    fi
else
    echo "❌ .env file not found"
fi
echo ""

# Try to fix common issues
echo "🔧 Attempting automatic fixes..."

# Fix Docker Compose version issues
if ! command -v docker-compose &> /dev/null; then
    echo "Installing docker-compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Fix permissions
echo "Fixing file permissions..."
sudo chown -R $USER:$USER .
chmod +x *.sh 2>/dev/null || true

echo ""
echo "🚀 Ready to try Docker Compose again!"
echo "======================================"
echo ""
echo "Try one of these commands:"
echo ""
echo "Option 1 (with docker-compose):"
echo "docker-compose -f docker-compose.prod.yml down"
echo "docker-compose -f docker-compose.prod.yml up --build -d"
echo ""
echo "Option 2 (with docker compose plugin):"
echo "docker compose -f docker-compose.prod.yml down"
echo "docker compose -f docker-compose.prod.yml up --build -d"
echo ""
echo "Option 3 (force rebuild):"
echo "docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans"
echo "docker-compose -f docker-compose.prod.yml build --no-cache"
echo "docker-compose -f docker-compose.prod.yml up -d"
