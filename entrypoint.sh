#!/bin/sh
set -e

# Run database initialization script
python init_db.py

# Run Gunicorn with optimized settings
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    run:app