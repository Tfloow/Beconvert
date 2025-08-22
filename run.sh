#!/bin/sh

# Check if .venv folder exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate the virtual environment
.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run
