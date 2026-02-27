#!/bin/bash
# Stop the running application
if [ -f /var/run/flask-app.pid ]; then
    PID=$(cat /var/run/flask-app.pid)
    echo "Stopping application with PID $PID..."
    kill -9 $PID 2>/dev/null || true
    rm -f /var/run/flask-app.pid
else
    echo "No PID file found, checking for running processes..."
    pkill -f "gunicorn.*hello:app" || true
fi
