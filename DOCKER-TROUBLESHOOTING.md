# 🔧 Docker Compose Error Fix Guide

## ❌ **Error Analysis**

The error `'ContainerConfig'` in Docker Compose typically indicates:

1. **Docker Compose version incompatibility**
2. **Corrupted container state**
3. **File permission issues**
4. **Conflicting container names**

## 🚀 **Step-by-Step Fix**

### **Step 1: Run the automated fix script**

```bash
# On your VPS, run:
./fix-docker.sh
```

### **Step 2: Manual cleanup (if needed)**

```bash
# Stop all related containers
docker stop $(docker ps -q --filter name=lookup-distance) 2>/dev/null

# Remove all related containers
docker rm $(docker ps -aq --filter name=lookup-distance) 2>/dev/null

# Remove related images
docker rmi $(docker images -q lookup-distance*) 2>/dev/null

# Clean up Docker system
docker system prune -f
```

### **Step 3: Try different Docker Compose commands**

```bash
# Option A: Standard docker-compose
docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans
docker-compose -f docker-compose.prod.yml up --build -d

# Option B: Docker compose plugin (newer)
docker compose -f docker-compose.prod.yml down --volumes --remove-orphans
docker compose -f docker-compose.prod.yml up --build -d

# Option C: Use compatible version
docker-compose -f docker-compose.compatible.yml down --volumes --remove-orphans
docker-compose -f docker-compose.compatible.yml up --build -d
```

### **Step 4: Check file integrity**

```bash
# Verify your app.py is clean
cat app.py | head -20

# Should show:
# from flask import Flask, request, jsonify
# import requests
# import os
# from dotenv import load_dotenv
# from flask_cors import CORS
```

### **Step 5: Verify requirements.txt**

```bash
# Check requirements
cat requirements.txt

# Should contain:
# Flask==2.3.3
# requests==2.31.0
# python-dotenv==1.0.0
# flask-cors==4.0.0
```

### **Step 6: Check .env file**

```bash
# Verify API key exists (don't print the actual key)
grep -q "GOOGLE_API_KEY" .env && echo "✅ API key found" || echo "❌ API key missing"
```

## 🔄 **Alternative: Simple Docker Run**

If Docker Compose continues to fail, try running with plain Docker:

```bash
# Build the image
docker build -t distance-lookup .

# Run the container
docker run -d \
  --name lookup-distance-service \
  -p 127.0.0.1:5001:5001 \
  --env-file .env \
  --restart unless-stopped \
  distance-lookup
```

## 📊 **Verify the fix**

```bash
# Check if container is running
docker ps

# Check logs
docker logs lookup-distance-service-prod

# Test the service
curl http://localhost:5001/distance?origin=test&destination=test
```

## 🆘 **If all else fails**

### **Reinstall Docker Compose**

```bash
# Remove old version
sudo apt remove docker-compose

# Install latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### **Use Docker Compose V2 (plugin)**

```bash
# Install Docker Compose plugin
sudo apt update
sudo apt install docker-compose-plugin

# Use new syntax
docker compose version
docker compose -f docker-compose.prod.yml up --build -d
```

## 🎯 **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| `ContainerConfig` error | Clean containers: `docker system prune -f` |
| Permission denied | Fix ownership: `sudo chown -R $USER:$USER .` |
| Port already in use | Find process: `sudo lsof -i :5001` |
| Out of disk space | Clean Docker: `docker system prune -a` |
| Version incompatibility | Use `docker-compose.compatible.yml` |

## ✅ **Success Checklist**

- [ ] Docker daemon running: `systemctl status docker`
- [ ] Clean app.py (no upload routes)
- [ ] Valid requirements.txt
- [ ] .env file with GOOGLE_API_KEY
- [ ] No conflicting containers
- [ ] Sufficient disk space
- [ ] Container running: `docker ps`
- [ ] Service responding: `curl localhost:5001/distance?origin=test&destination=test`

---

🎉 **Once fixed, your service will be available at `https://distance.lookupferrara.it`**
