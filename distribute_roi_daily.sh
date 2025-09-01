#!/bin/bash

# Navigate to your project directory
cd /home/infinitytrade

# Activate the virtual environment
source infinityenv/bin/activate

# Run the Django custom command
python3 manage.py distribute_daily_roi
