#!/bin/bash
cd /home/ec2-user/flask-app

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Set proper permissions
chown -R ec2-user:ec2-user /home/ec2-user/flask-app
chmod +x scripts/*.sh
