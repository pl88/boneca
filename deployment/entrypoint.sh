#!/bin/bash
set -e

echo "🚀 Starting Boneca Deployment in production mode..."

# Start the application
exec uvicorn src.deployment:app --host 0.0.0.0 --port 8001
