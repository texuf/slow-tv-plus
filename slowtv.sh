#!/bin/bash

# Configuration
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$APP_DIR/src/player.py"
PID_FILE="$APP_DIR/slowtv.pid"
LOG_FILE="$APP_DIR/logs/slowtv.log"
URL_FILE="$APP_DIR/urls.txt"

# Function to start the application
start() {
    if [ -f "$PID_FILE" ]; then
        echo "SlowTV+ is already running."
        return 1
    fi
    
    echo "Starting SlowTV+..."
    python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "SlowTV+ started. PID: $(cat "$PID_FILE")"
}

# Function to stop the application
stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "SlowTV+ is not running."
        return 1
    fi
    
    echo "Stopping SlowTV+..."
    kill $(cat "$PID_FILE")
    rm "$PID_FILE"
    echo "SlowTV+ stopped."
}

# Function to update the application
update() {
    echo "Updating SlowTV+..."
    git pull origin main
    pip3 install -r requirements.txt
    echo "Update complete."
}

# Main command handler
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    update)
        update
        ;;
    *)
        echo "Usage: $0 {start|stop|update}"
        exit 1
        ;;
esac
