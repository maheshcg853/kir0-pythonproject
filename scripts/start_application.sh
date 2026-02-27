#!/bin/bash
cd /home/ec2-user/flask-app

# Start application with Gunicorn
echo "Starting Flask application..."
export PORT=5000
nohup gunicorn -w 4 -b 0.0.0.0:5000 hello:app > /var/log/flask-app.log 2>&1 &

echo $! > /var/run/flask-app.pid
echo "Application started with PID $(cat /var/run/flask-app.pid)"
