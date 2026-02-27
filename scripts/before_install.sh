#!/bin/bash
# Stop and remove old application if exists
if [ -d "/home/ec2-user/flask-app" ]; then
    echo "Removing old application files..."
    rm -rf /home/ec2-user/flask-app
fi

# Install Python and pip
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    yum install -y python3
fi

if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    yum install -y python3-pip
fi

echo "Python version: $(python3 --version)"
echo "Pip version: $(pip3 --version)"
