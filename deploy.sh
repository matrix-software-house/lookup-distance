#!/bin/bash

# Deployment script for Flask Distance Lookup Service on VPS
# Domain: distance.lookupferrara.it

set -e

# Configuration
DOMAIN="distance.lookupferrara.it"
APP_DIR="/opt/lookup-distance"
NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
SERVICE_NAME="lookup-distance"

echo "🚀 Deploying Flask Distance Lookup Service"
echo "================================="
echo "Domain: $DOMAIN"
echo "App Directory: $APP_DIR"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)" 
   exit 1
fi

echo "📦 Step 1: Installing dependencies..."
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y nginx docker.io docker-compose certbot python3-certbot-nginx ufw git

# Start and enable services
systemctl start docker
systemctl enable docker
systemctl start nginx
systemctl enable nginx

echo "🔥 Step 2: Setting up firewall..."
# Configure UFW firewall
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

echo "📁 Step 3: Creating application directory..."
# Create app directory
mkdir -p $APP_DIR
cd $APP_DIR

echo "📋 Step 4: Setting up application files..."
# You'll need to copy your application files here
echo "ℹ️  Please copy your application files to $APP_DIR"
echo "   Required files:"
echo "   - app.py"
echo "   - docker-compose.yml"
echo "   - Dockerfile"
echo "   - requirements.txt"
echo "   - .env (with your GOOGLE_API_KEY)"
echo ""

echo "🌐 Step 5: Setting up Nginx configuration..."
# Copy nginx configuration
cp nginx.conf $NGINX_CONF_DIR/$DOMAIN

# Enable the site
ln -sf $NGINX_CONF_DIR/$DOMAIN $NGINX_ENABLED_DIR/

# Remove default nginx site
rm -f $NGINX_ENABLED_DIR/default

# Test nginx configuration
nginx -t

echo "🔒 Step 6: Setting up SSL certificate..."
# Get SSL certificate
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo "🐳 Step 7: Starting Docker services..."
# Start the Flask application
cd $APP_DIR
docker-compose up -d --build

echo "🔄 Step 8: Reloading services..."
# Reload nginx
systemctl reload nginx

# Create systemd service for auto-start
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Flask Distance Lookup Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl enable $SERVICE_NAME.service
systemctl daemon-reload

echo "📊 Step 9: Setting up monitoring..."
# Create log rotation
cat > /etc/logrotate.d/nginx-$DOMAIN << EOF
/var/log/nginx/$DOMAIN.*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 nginx nginx
    postrotate
        systemctl reload nginx
    endscript
}
EOF

echo "✅ Deployment completed successfully!"
echo ""
echo "🌍 Your service should now be available at: https://$DOMAIN"
echo ""
echo "📋 Next steps:"
echo "1. Copy your application files to $APP_DIR"
echo "2. Make sure your .env file contains the GOOGLE_API_KEY"
echo "3. Test the service: curl https://$DOMAIN/distance?origin=test&destination=test"
echo ""
echo "📊 Useful commands:"
echo "- Check service status: systemctl status $SERVICE_NAME"
echo "- View logs: docker-compose -f $APP_DIR/docker-compose.yml logs -f"
echo "- Restart service: systemctl restart $SERVICE_NAME"
echo "- Check nginx status: systemctl status nginx"
echo "- Renew SSL: certbot renew"
echo ""
echo "🔍 Troubleshooting:"
echo "- Check nginx config: nginx -t"
echo "- Check nginx error log: tail -f /var/log/nginx/$DOMAIN.error.log"
echo "- Check docker containers: docker ps"
echo ""
echo "🎉 Deployment complete!"
