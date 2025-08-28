#!/bin/sh

# Run database initialization script
python init_db.py

# Run Gunicorn to serve Flask app
exec gunicorn --bind 0.0.0.0:5000 --workers 2 run:app