#!/usr/bin/env python3
"""
CMMC Level 2 Compliance Tracker
Run script to start the Flask application
"""

import os
import sys

# Add the app directory to the Python path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
sys.path.insert(0, app_dir)

from main import app

if __name__ == '__main__':
    print("Starting CMMC Level 2 Compliance Tracker...")
    print("Access the application at: http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server")
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    app.run(debug=True, host='127.0.0.1', port=8080)
