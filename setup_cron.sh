#!/bin/bash

# CoinFlow - Automated Daily Data Update Setup
# This script sets up a cron job to refresh crypto data daily

COINFLOW_DIR="/Users/rohita/nyc_taxi_jan_2025_pipeline/coinflow"
LOG_DIR="$COINFLOW_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Cron job command (runs daily at 9 AM)
CRON_CMD="0 9 * * * cd $COINFLOW_DIR && make run-pipeline >> $LOG_DIR/pipeline.log 2>&1 && make dbt-run >> $LOG_DIR/dbt.log 2>&1"

echo " CoinFlow Cron Setup"
echo "====================="
echo ""
echo "This will set up a daily cron job to:"
echo "  1. Fetch latest crypto data (9:00 AM daily)"
echo "  2. Run dbt transformations"
echo "  3. Log output to $LOG_DIR"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "coinflow"; then
    echo "  A CoinFlow cron job already exists!"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep coinflow
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo " Cancelled. No changes made."
        exit 0
    fi
    # Remove existing coinflow cron jobs
    crontab -l | grep -v coinflow | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo ""
echo " Cron job installed successfully!"
echo ""
echo "📋 Your CoinFlow cron job:"
echo "$CRON_CMD"
echo ""
echo " Logs will be saved to:"
echo "  - Pipeline: $LOG_DIR/pipeline.log"
echo "  - dbt: $LOG_DIR/dbt.log"
echo ""
echo " To view your cron jobs:"
echo "  crontab -l"
echo ""
echo "  To remove the cron job:"
echo "  crontab -e  (then delete the coinflow line)"
echo ""
echo " Done! Your dashboard will auto-update daily at 9:00 AM."
