FROM python:3.11-slim

WORKDIR /app

# Install Poetry and other required packages
RUN pip install poetry && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Poetry files
COPY pyproject.toml ./

# Generate poetry.lock if it doesn't exist and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --without dev --no-root --no-interaction --no-ansi

# Copy poetry.lock if it exists
COPY poetry.lock* ./

# Copy application code
COPY src/ ./src/

# Make entrypoint scripts executable
COPY src/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
