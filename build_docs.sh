#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install requirements if not already installed
pip install -r requirements.txt

# Run the documentation setup script
python setup_docs.py 