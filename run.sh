#!/bin/bash

# Install requirements if needed
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Check if virtualenv is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed!"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install or update requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run the Streamlit app
echo "Starting Toko Pintar application..."
streamlit run app.py