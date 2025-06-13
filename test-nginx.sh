#!/bin/bash

# Nginx configuration test script for VPS deployment
# Run this on your VPS to test the nginx configuration

DOMAIN="distance.lookupferrara.it"
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"

echo "🔍 Testing Nginx configuration for $DOMAIN"
echo "========================================"

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "❌ Nginx is not installed"
    exit 1
fi

echo "✅ Nginx is installed"

# Check if configuration file exists
if [ ! -f "$NGINX_CONF" ]; then
    echo "❌ Configuration file not found: $NGINX_CONF"
    exit 1
fi

echo "✅ Configuration file exists: $NGINX_CONF"

# Test nginx configuration
echo "🧪 Testing nginx configuration syntax..."
if nginx -t; then
    echo "✅ Nginx configuration syntax is valid"
else
    echo "❌ Nginx configuration has syntax errors"
    echo "📋 Check the error messages above and fix the configuration"
    exit 1
fi

# Check if site is enabled
NGINX_ENABLED="/etc/nginx/sites-enabled/$DOMAIN"
if [ -L "$NGINX_ENABLED" ]; then
    echo "✅ Site is enabled: $NGINX_ENABLED"
else
    echo "⚠️  Site is not enabled. Enable it with:"
    echo "   sudo ln -s $NGINX_CONF $NGINX_ENABLED"
fi

# Check nginx service status
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx service is running"
else
    echo "⚠️  Nginx service is not running. Start it with:"
    echo "   sudo systemctl start nginx"
fi

echo ""
echo "🎉 Nginx configuration test completed!"
echo ""
echo "📋 Next steps:"
echo "1. If there were syntax errors, fix them in: $NGINX_CONF"
echo "2. Reload nginx: sudo systemctl reload nginx"
echo "3. Test your domain: curl -I https://$DOMAIN"
