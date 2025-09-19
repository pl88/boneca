# Database Migrations with Alembic

This document explains how to use Alembic for database migrations in the Boneca project.

## Overview

Alembic is a lightweight database migration tool for usage with SQLAlchemy. It provides:
- Version control for database schema changes
- Automatic migration script generation
- Forward and backward migration support
- Integration with SQLAlchemy models

## Setup

The Alembic configuration is already set up and integrated with our application settings:

- **Configuration**: `alembic.ini` and `alembic/env.py`
- **Database URL**: Automatically configured from `src/core/config.py`
- **Schema**: Uses the `boneca` schema as configured in environment variables
- **Migration files**: Stored in `alembic/versions/` with timestamp naming

## Quick Start

### Starting Database and Services

```bash
# Start the database
make db-up

# Start the development environment
make run-dev
```

### Basic Migration Commands

```bash
# Check current migration status
make migrate-status

# Create a new migration
make migrate-create MSG="Add user table"

# Run pending migrations
make migrate-up

# Show migration history
make migrate-history
```

## Available Commands

### Creating Migrations

```bash
# Create a new migration with autogenerate (requires SQLAlchemy models)
make migrate-create MSG="Your migration description"

# Example:
make migrate-create MSG="Add user authentication tables"
```

### Running Migrations

```bash
# Run all pending migrations to the latest
make migrate-up

# Roll back one migration
make migrate-down

# Roll back to a specific revision
make migrate-down REVISION="abc123"

# Reset all migrations (careful!)
make migrate-reset
```

### Migration Information

```bash
# Check current migration status
make migrate-status

# Show migration history
make migrate-history

# Show details of a specific migration
make migrate-show REVISION="abc123"

# Manually stamp database with a revision (advanced)
make migrate-stamp REVISION="head"
```

## Migration File Structure

Migration files are stored in `alembic/versions/` with the naming pattern:
```
YYYY_MM_DD_HHMM_<revision_id>_<description>.py
```

Example: `2025_09_19_1400_859efdfc3f9f_initial_migration_setup.py`

Each migration file contains:
- `upgrade()`: Function to apply the migration
- `downgrade()`: Function to reverse the migration
- Metadata about the revision

## Integration with Application

### Environment Configuration

Alembic automatically uses your application configuration:

```python
# From src/core/config.py
DATABASE_HOST=postgres      # or localhost
DATABASE_PORT=5432
DATABASE_NAME=boneca
DATABASE_USER=boneca
DATABASE_PASSWORD=boneca
DATABASE_SCHEMA=boneca
```

### Database Utilities

Use the `DatabaseConfig` class for migration-related operations:

```python
from src.core.database import DatabaseConfig

# Get Alembic configuration
config = DatabaseConfig.get_alembic_config()

# Get migration connection arguments
args = DatabaseConfig.get_migration_connection_args()
```

## Best Practices

### Migration Naming

Use descriptive names for your migrations:
```bash
# Good
make migrate-create MSG="Add user authentication tables"
make migrate-create MSG="Add indexes for performance"
make migrate-create MSG="Modify user table for GDPR compliance"

# Less descriptive
make migrate-create MSG="Update database"
make migrate-create MSG="Fix stuff"
```

### Testing Migrations

Always test your migrations in both directions:

```bash
# Apply the migration
make migrate-up

# Test that it works
make db-test

# Roll back to test the downgrade
make migrate-down

# Apply again to ensure repeatability
make migrate-up
```

### Migration Content

1. **Data migrations**: Include data transformation logic when needed
2. **Indexes**: Add indexes for performance-critical queries
3. **Constraints**: Add foreign keys and check constraints
4. **Schema changes**: Add/remove/modify tables and columns

Example migration structure:
```python
def upgrade() -> None:
    """Upgrade schema."""
    # Create table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        schema='boneca'
    )
    
    # Add index
    op.create_index('ix_users_email', 'users', ['email'], schema='boneca')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users', schema='boneca')
```

## Troubleshooting

### Common Issues

1. **Permission denied errors**: Ensure the database user has necessary permissions
2. **Schema not found**: Check that the `boneca` schema exists and is accessible
3. **Connection errors**: Verify database connection settings in `.env` file

### Recovery Commands

```bash
# Check database connection
make db-test

# View current database state
make db-connect
\dt boneca.*

# Reset migration state (advanced)
make migrate-stamp REVISION="base"
```

### Environment Differences

The migration system works in different environments:

- **Local Docker**: Uses `postgres` as database host
- **CI/CD**: May use `localhost` as database host
- **Production**: Configure appropriate database settings

## Integration with Development Workflow

### Typical Development Flow

1. Make changes to your SQLAlchemy models
2. Generate migration: `make migrate-create MSG="Description"`
3. Review the generated migration file
4. Test the migration: `make migrate-up`
5. Commit both model changes and migration file
6. Deploy to staging/production

### Code Review

When reviewing migrations:
- Check both `upgrade()` and `downgrade()` functions
- Verify schema changes match the intended design
- Ensure data transformation logic is correct
- Test migrations on a copy of production data

## Advanced Usage

### Manual Migration Creation

For complex migrations, you may need to create migrations manually:

```bash
# Create an empty migration
docker compose -p boneca exec boneca-dev poetry run alembic revision -m "Manual migration"
```

Then edit the generated file to add your custom logic.

### Multiple Migration Paths

For complex schema evolution, you might need branching:

```bash
# Create a branch point
docker compose -p boneca exec boneca-dev poetry run alembic revision -m "Branch point"

# Create migrations from different points
docker compose -p boneca exec boneca-dev poetry run alembic revision --head=abc123 -m "Branch A"
docker compose -p boneca exec boneca-dev poetry run alembic revision --head=abc123 -m "Branch B"
```

## Production Considerations

### Deployment Strategy

1. **Test migrations** on a production-like database
2. **Backup database** before applying migrations
3. **Apply migrations** during maintenance windows when possible
4. **Monitor performance** of migration operations
5. **Have rollback plan** ready

### Large Table Migrations

For large tables, consider:
- Running migrations during low-traffic periods
- Using online schema change tools for zero-downtime
- Breaking large migrations into smaller chunks
- Adding indexes concurrently when possible

## Further Reading

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)