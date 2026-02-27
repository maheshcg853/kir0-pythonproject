#!/bin/bash
cd /home/ec2-user/flask-app

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Verify gunicorn installation
if command -v gunicorn &> /dev/null; then
    echo "Gunicorn installed at: $(which gunicorn)"
else
    echo "Gunicorn not found in PATH, checking pip3 location..."
    pip3 show gunicorn
fi

# Set proper permissions
chown -R ec2-user:ec2-user /home/ec2-user/flask-app
chmod +x scripts/*.sh
