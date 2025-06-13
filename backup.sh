#!/bin/bash

# Backup script for Flask Distance Lookup Service
# Creates backups of application files, configuration, and data

BACKUP_DIR="/opt/backups/lookup-distance"
APP_DIR="/opt/lookup-distance"
DOMAIN="distance.lookupferrara.it"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="lookup-distance-backup-$DATE.tar.gz"

# Create backup directory
mkdir -p $BACKUP_DIR

echo "🗂️  Creating backup: $BACKUP_FILE"

# Create backup
cd /opt
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude="lookup-distance/__pycache__" \
    --exclude="lookup-distance/.git" \
    lookup-distance \
    /etc/nginx/sites-available/$DOMAIN \
    /etc/systemd/system/lookup-distance.service \
    /etc/letsencrypt/live/$DOMAIN 2>/dev/null || true

echo "✅ Backup created: $BACKUP_DIR/$BACKUP_FILE"

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t lookup-distance-backup-*.tar.gz | tail -n +8 | xargs -r rm

echo "🧹 Old backups cleaned up"
echo "📊 Current backups:"
ls -lah $BACKUP_DIR/lookup-distance-backup-*.tar.gz
