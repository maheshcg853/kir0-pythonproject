#!/bin/bash
# Stop and remove old application if exists
if [ -d "/home/ec2-user/flask-app" ]; then
    echo "Removing old application files..."
    rm -rf /home/ec2-user/flask-app
fi

# Install Python and pip if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    yum install -y python3 python3-pip
fi
