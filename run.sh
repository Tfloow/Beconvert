#!/bin/bash
set -e

echo "Installing system dependencies..."


# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

echo "All dependencies installed."