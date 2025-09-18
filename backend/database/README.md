# PostgreSQL Database Setup

This directory contains the PostgreSQL database setup for the Boneca project.

## Database Configuration

- **Database Name**: `boneca`
- **Schema Name**: `boneca`
- **Admin User**: `postgres` / `postgres` (for development)
- **Application User**: `boneca` / `boneca` (read/write access)

## Setup Instructions

1. **Start Docker daemon** (if not already running):

   ```bash
   sudo systemctl start docker
   ```

2. **Start PostgreSQL service**:

   ```bash
   # Using Makefile (recommended)
   make db-up
   ```

3. **Test the setup**:

   ```bash
   make db-test
   ```

## Database Structure

- **Port**: 5432 (mapped to host)
- **Volume**: `boneca-postgres-data` (persistent storage)
- **Initialization**: Scripts in `database/init/` are executed on first startup

## Connection Details

### Admin Connection
```
Host: localhost
Port: 5432
Database: boneca
Username: postgres
Password: postgres
```

### Application Connection
```
Host: localhost
Port: 5432
Database: boneca
Schema: boneca
Username: boneca
Password: boneca
```

## Makefile Commands

```bash
# Database management
make db-up            # Start PostgreSQL database  
make db-down          # Stop PostgreSQL database
make db-status        # Check database status
make db-logs          # View database logs
make db-test          # Test database setup and connections
make db-connect       # Connect to database as boneca user
make db-connect-admin # Connect to database as admin (postgres)
make db-clean         # Stop database and remove volumes
```

## Files

- `docker-compose.yml`: Contains PostgreSQL service definition
- `database/init/01-init-database.sql`: Creates database, schema, and users
- `Makefile`: Contains database management targets

## Direct Docker Commands (if needed)

```bash
# Start only PostgreSQL
docker-compose --profile dev up postgres -d

# Stop PostgreSQL
docker-compose down

# View logs
docker-compose logs postgres

# Connect to PostgreSQL container
docker-compose exec postgres psql -U postgres -d boneca

# Connect as boneca user
docker-compose exec postgres psql -U boneca -d boneca
```