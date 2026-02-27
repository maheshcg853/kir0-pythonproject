#!/bin/bash
cd /home/ec2-user/flask-app

# Start application with Gunicorn as ec2-user
echo "Starting Flask application..."
export PORT=5000

# Run as ec2-user and keep process alive
su - ec2-user -c "cd /home/ec2-user/flask-app && nohup gunicorn -w 4 -b 0.0.0.0:5000 hello:app > /var/log/flask-app.log 2>&1 & echo \$! > /var/run/flask-app.pid"

sleep 2

if [ -f /var/run/flask-app.pid ]; then
    PID=$(cat /var/run/flask-app.pid)
    if ps -p $PID > /dev/null; then
        echo "Application started successfully with PID $PID"
    else
        echo "Application failed to start. Check /var/log/flask-app.log"
        exit 1
    fi
else
    echo "PID file not created"
    exit 1
fi
