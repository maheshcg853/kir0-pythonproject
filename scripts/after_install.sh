#!/bin/bash
cd /home/ec2-user/flask-app

# Install dependencies as ec2-user
echo "Installing Python dependencies..."
su - ec2-user -c "cd /home/ec2-user/flask-app && pip3 install --user -r requirements.txt"

# Set proper permissions
chown -R ec2-user:ec2-user /home/ec2-user/flask-app
chmod +x scripts/*.sh
