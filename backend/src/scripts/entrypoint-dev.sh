#!/bin/bash
set -e

echo "🛠️  Starting Boneca API in development mode..."

# Wait for any dependencies here if needed
# Example: wait-for-it.sh db:5432 -t 60

# Run any migrations here if needed
# Example: alembic upgrade head

# Start the application in development mode with hot reload
exec uvicorn src.main:boneca --host 0.0.0.0 --port 8000 --reload
