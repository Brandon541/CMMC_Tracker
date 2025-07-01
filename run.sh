#!/bin/bash

# CMMC Compliance Tracker Launcher
echo "Starting CMMC Level 2 Compliance Tracker..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting Flask application..."
echo "Open your browser to http://localhost:8080"
python app/main.py
