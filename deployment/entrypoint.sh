#!/bin/bash
set -e

echo "🚀 Starting Boneca Deployment in production mode..."

# Start the application
exec gunicorn src.deployment:app --bind 0.0.0.0:8001
