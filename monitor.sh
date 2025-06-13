#!/bin/bash

# Health monitoring script for Flask Distance Lookup Service
# Usage: ./monitor.sh

DOMAIN="distance.lookupferrara.it"
APP_DIR="/opt/lookup-distance"
LOG_FILE="/var/log/lookup-distance-monitor.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Function to check service health
check_health() {
    local url="https://$DOMAIN/distance?origin=test&destination=test"
    local response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    
    if [ "$response" = "200" ]; then
        return 0
    else
        return 1
    fi
}

# Function to restart service
restart_service() {
    log "🔄 Attempting to restart service..."
    cd $APP_DIR
    docker-compose -f docker-compose.prod.yml down
    sleep 5
    docker-compose -f docker-compose.prod.yml up -d
    sleep 10
}

# Function to send notification (customize as needed)
send_notification() {
    local message="$1"
    log "📧 Notification: $message"
    # Add your notification method here (email, Slack, Discord, etc.)
    # Example for email:
    # echo "$message" | mail -s "Service Alert: $DOMAIN" admin@yourdomain.com
}

# Main monitoring logic
main() {
    log "🔍 Checking service health..."
    
    if check_health; then
        log "✅ Service is healthy"
        # Reset failure counter if exists
        rm -f /tmp/service_failures 2>/dev/null
    else
        log "❌ Service health check failed"
        
        # Count failures
        if [ -f /tmp/service_failures ]; then
            failures=$(cat /tmp/service_failures)
            failures=$((failures + 1))
        else
            failures=1
        fi
        echo $failures > /tmp/service_failures
        
        log "⚠️  Failure count: $failures"
        
        # Restart after 2 consecutive failures
        if [ $failures -ge 2 ]; then
            log "🚨 Multiple failures detected, restarting service..."
            restart_service
            
            # Wait and check again
            sleep 30
            if check_health; then
                log "✅ Service recovered after restart"
                send_notification "Service $DOMAIN recovered after restart"
                rm -f /tmp/service_failures
            else
                log "❌ Service still unhealthy after restart"
                send_notification "CRITICAL: Service $DOMAIN failed to recover after restart"
            fi
        fi
    fi
}

# Run the check
main
