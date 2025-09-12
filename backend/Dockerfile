FROM python:3.13-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only production files
COPY pyproject.toml poetry.lock* ./
COPY src/ ./src/

# Install only production dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Copy and set up entrypoint
COPY src/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
