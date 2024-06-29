#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run your Python script
python3 main.py

# Deactivate virtual environment (optional)
deactivate