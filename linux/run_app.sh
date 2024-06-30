#!/bin/bash

# Create Virtual enviroment
# Refer as venv
python3 -m venv venv 

# Activate venv 
source venv/bin/activate

# Upgrade pip module
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Run the application
python3 main.py

# Deactivate venv
deactivate
