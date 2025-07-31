#!/bin/bash

# Critical Values Alert System - Startup Script
# This script ensures the Streamlit app runs with optimal settings

echo "Starting Critical Values Alert System..."

# Set environment variables for better stability
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Kill any existing Streamlit processes on port 8501
echo "Checking for existing processes..."
lsof -ti:8501 | xargs kill -9 2>/dev/null || true

# Install watchdog if not already installed (for better file monitoring)
echo "Checking dependencies..."
pip install watchdog >/dev/null 2>&1 || true

# Run the Streamlit app with specific settings
echo "Launching dashboard on http://localhost:8501"
streamlit run app.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless true \
    --browser.serverAddress localhost \
    --browser.gatherUsageStats false \
    --server.runOnSave true \
    --server.allowRunOnSave true \
    --server.fileWatcherType auto