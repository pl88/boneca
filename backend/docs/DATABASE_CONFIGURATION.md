# Database Configuration Guide

This document explains how to configure and use the database connection in the Boneca application.

## Configuration Files

### `.env.example`
Template file with all available configuration options and their default values. This file is committed to version control.

### `.env`
Local environment configuration file. Copy from `.env.example` and modify as needed. This file is not committed to version control.

## Database Settings

The following environment variables control database connectivity:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DATABASE_HOST` | PostgreSQL server hostname | `postgres` | `localhost`, `db.example.com` |
| `DATABASE_PORT` | PostgreSQL server port | `5432` | `5432`, `5433` |
| `DATABASE_NAME` | Database name | `boneca` | `boneca_dev`, `my_app` |
| `DATABASE_USER` | Database username | `boneca` | `app_user`, `developer` |
| `DATABASE_PASSWORD` | Database password | `boneca` | `secure_password123` |
| `DATABASE_SCHEMA` | Default schema name | `boneca` | `public`, `app_schema` |

## Environment-Specific Configuration

### Docker Development (Recommended)
When running in Docker containers, use the service name as the host:

```bash
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=boneca
DATABASE_USER=boneca
DATABASE_PASSWORD=boneca
DATABASE_SCHEMA=boneca
```

### Local Development (Outside Docker)
When running locally without Docker, use localhost:

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=boneca
DATABASE_USER=boneca
DATABASE_PASSWORD=boneca
DATABASE_SCHEMA=boneca
```

### Production
For production environments, use secure credentials and the actual database server:

```bash
DATABASE_HOST=prod-db.company.com
DATABASE_PORT=5432
DATABASE_NAME=boneca_prod
DATABASE_USER=boneca_app
DATABASE_PASSWORD=very_secure_password_123
DATABASE_SCHEMA=boneca
```

## Using Database Configuration in Code

### Basic Usage

```python
from src.core.config import settings
from src.core.database import DatabaseConfig

# Get individual settings
host = settings.DATABASE_HOST
port = settings.DATABASE_PORT
db_name = settings.DATABASE_NAME

# Get connection URL
url = settings.DATABASE_URL
# Returns: postgresql://boneca:boneca@postgres:5432/boneca

# Get connection parameters for libraries like psycopg2
params = DatabaseConfig.get_connection_params()
# Returns: {'host': 'postgres', 'port': 5432, 'database': 'boneca', ...}
```

### Connection Examples

#### Using psycopg2
```python
import psycopg2
from src.core.database import DatabaseConfig

# Option 1: Using connection URL
conn = psycopg2.connect(DatabaseConfig.get_connection_url())

# Option 2: Using individual parameters
params = DatabaseConfig.get_connection_params()
conn = psycopg2.connect(**params)
```

#### Using SQLAlchemy
```python
from sqlalchemy import create_engine
from src.core.database import DatabaseConfig

engine = create_engine(DatabaseConfig.get_connection_url())
```

#### Using asyncpg
```python
import asyncpg
from src.core.database import DatabaseConfig

conn = await asyncpg.connect(DatabaseConfig.get_connection_url())
```

## Setup Instructions

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Modify `.env` for your environment:**
   - For Docker development: Use `DATABASE_HOST=postgres`
   - For local development: Use `DATABASE_HOST=localhost`
   - Update credentials as needed

3. **Start the database:**
   ```bash
   make db-up
   ```

4. **Test the configuration:**
   ```bash
   make db-test
   ```

## Testing

The configuration is fully tested and supports:
- Default value testing
- Environment variable override testing
- Connection parameter generation testing
- URL construction testing

Run tests with:
```bash
make test PYTEST_ARGS="tests/core/test_config.py tests/core/test_database.py"
```

## Security Notes

- Never commit `.env` files to version control
- Use strong passwords in production
- Consider using environment-specific secrets management
- Rotate database passwords regularly
- Use SSL/TLS connections in production (add `?sslmode=require` to connection URLs)

## Troubleshooting

### Connection Issues
1. Check that the database service is running: `make db-status`
2. Verify environment variables are loaded correctly
3. Ensure host/port are accessible from your application environment
4. Check firewall and network connectivity

### Configuration Issues
1. Verify `.env` file exists and has correct values
2. Check that environment variables match expected names (case-sensitive)
3. Ensure no trailing spaces in `.env` values
4. Restart application after changing `.env` file