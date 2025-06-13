# 🌐 VPS Deployment Guide

Complete guide for deploying your Flask Distance Lookup Service to a VPS with domain `distance.lookupferrara.it`.

## 📋 Prerequisites

- Ubuntu/Debian VPS with root access
- Domain `distance.lookupferrara.it` pointing to your VPS IP
- Google Maps API key with Distance Matrix API enabled

## 🚀 Quick Deployment

### 1. Prepare your VPS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install git
sudo apt install -y git
```

### 2. Upload your project files

```bash
# Copy all project files to your VPS
scp -r /Users/iwan/dev/python/lookup_distance root@your-vps-ip:/tmp/

# Or clone from git if you have a repository
# git clone your-repo-url /opt/lookup-distance
```

### 3. Run the deployment script

```bash
# On your VPS, run as root
sudo bash /tmp/lookup_distance/deploy.sh
```

## 📁 File Structure on VPS

```
/opt/lookup-distance/           # Main application directory
├── app.py                      # Flask application
├── docker-compose.prod.yml     # Production Docker Compose
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (GOOGLE_API_KEY)
├── nginx.conf                  # Nginx configuration
├── deploy.sh                   # Deployment script
└── monitor.sh                  # Health monitoring script

/etc/nginx/sites-available/     # Nginx configurations
└── distance.lookupferrara.it     # Your site configuration

/var/log/nginx/                 # Nginx logs
├── distance.lookupferrara.it.access.log
└── distance.lookupferrara.it.error.log
```

## 🔧 Manual Configuration Steps

### 1. Create .env file

```bash
# On your VPS
echo "GOOGLE_API_KEY=your_actual_google_api_key_here" > /opt/lookup-distance/.env
```

### 2. Start the service

```bash
cd /opt/lookup-distance
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

### 3. Verify deployment

```bash
# Check if containers are running
sudo docker ps

# Check service health
curl https://distance.lookupferrara.it/distance?origin=test&destination=test

# Check nginx status
sudo systemctl status nginx
```

## 📊 Monitoring & Maintenance

### Set up automated monitoring

```bash
# Add to crontab for health checks every 5 minutes
sudo crontab -e

# Add this line:
*/5 * * * * /opt/lookup-distance/monitor.sh
```

### Useful commands

```bash
# View application logs
sudo docker-compose -f /opt/lookup-distance/docker-compose.prod.yml logs -f

# Restart the service
sudo systemctl restart lookup-distance

# Check nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# View nginx error logs
sudo tail -f /var/log/nginx/distance.lookupferrara.it.error.log

# View nginx access logs
sudo tail -f /var/log/nginx/distance.lookupferrara.it.access.log

# Check SSL certificate
sudo certbot certificates

# Renew SSL certificate
sudo certbot renew --dry-run
```

## 🔒 Security Features

The Nginx configuration includes:

- ✅ **SSL/TLS encryption** with Let's Encrypt
- ✅ **Security headers** (HSTS, XSS protection, etc.)
- ✅ **Rate limiting** (10 requests/second with burst of 20)
- ✅ **CORS support** for web applications
- ✅ **Request filtering** (blocks suspicious patterns)
- ✅ **Firewall configuration** (UFW)

## 🌍 Testing Your Deployed Service

### API Endpoints

```bash
# Basic distance lookup
curl "https://distance.lookupferrara.it/distance?origin=New+York,NY&destination=Boston,MA"

# Health check
curl "https://distance.lookupferrara.it/health"

# International locations
curl "https://distance.lookupferrara.it/distance?origin=London,UK&destination=Paris,France"
```

### Browser Testing

Visit these URLs in your browser:
- https://distance.lookupferrara.it/distance?origin=New%20York,%20NY&destination=Boston,%20MA
- https://distance.lookupferrara.it/health

## 🔍 Troubleshooting

### Service not responding

```bash
# Check if containers are running
sudo docker ps

# Check container logs
sudo docker-compose -f /opt/lookup-distance/docker-compose.prod.yml logs

# Restart containers
sudo docker-compose -f /opt/lookup-distance/docker-compose.prod.yml restart
```

### SSL certificate issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Test nginx configuration
sudo nginx -t
```

### High CPU/Memory usage

```bash
# Check system resources
htop

# Check Docker container stats
sudo docker stats

# Check nginx status
sudo systemctl status nginx
```

## 📈 Performance Optimization

### For high traffic, consider:

1. **Load balancing**: Add multiple Flask instances
2. **Caching**: Implement Redis for API response caching
3. **Database**: Add persistent storage for analytics
4. **CDN**: Use CloudFlare for static content
5. **Monitoring**: Set up Prometheus + Grafana

### Example load balancer configuration

```nginx
upstream flask_backend {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

## 🎯 Production Checklist

- ✅ Domain DNS configured
- ✅ SSL certificate installed
- ✅ Firewall configured
- ✅ Application deployed
- ✅ Health monitoring enabled
- ✅ Log rotation configured
- ✅ Backup strategy planned
- ✅ API rate limiting enabled
- ✅ Security headers configured

## 📞 Support

Your Flask Distance Lookup Service is now production-ready at:
**https://distance.lookupferrara.it**

The service includes:
- 🔒 SSL encryption
- 🛡️ Security headers and rate limiting  
- 📊 Health monitoring
- 🔄 Auto-restart on failure
- 📝 Comprehensive logging
- 🌐 CORS support for web apps

---

🎉 **Your service is ready for production use!**
