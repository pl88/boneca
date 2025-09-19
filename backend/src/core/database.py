"""Database connection utility module.

This module provides utilities for connecting to the PostgreSQL database
using the application configuration.
"""
from typing import Any, Dict

from src.core.config import settings


class DatabaseConfig:
    """Database configuration helper class."""

    @staticmethod
    def get_connection_params() -> dict[str, str | int]:
        """Get database connection parameters as a dictionary.

        Returns:
            Dictionary containing database connection parameters.
        """
        return {
            "host": settings.DATABASE_HOST,
            "port": settings.DATABASE_PORT,
            "database": settings.DATABASE_NAME,
            "user": settings.DATABASE_USER,
            "password": settings.DATABASE_PASSWORD,
            "options": f"-c search_path={settings.DATABASE_SCHEMA}",
        }

    @staticmethod
    def get_connection_url() -> str:
        """Get the complete database connection URL.

        Returns:
            PostgreSQL connection URL string.
        """
        return settings.DATABASE_URL

    @staticmethod
    def get_schema_name() -> str:
        """Get the database schema name.

        Returns:
            Database schema name.
        """
        return settings.DATABASE_SCHEMA

    @staticmethod
    def get_alembic_config() -> Dict[str, Any]:
        """Get Alembic-specific database configuration.

        Returns:
            Dictionary containing Alembic configuration parameters.
        """
        return {
            "sqlalchemy.url": settings.DATABASE_URL,
            "target_schema": settings.DATABASE_SCHEMA,
            "version_table_schema": settings.DATABASE_SCHEMA,
            "include_schemas": True,
        }

    @staticmethod
    def get_migration_connection_args() -> Dict[str, Any]:
        """Get connection arguments for migration operations.

        Returns:
            Dictionary containing connection arguments for SQLAlchemy.
        """
        return {
            "options": f"-csearch_path={settings.DATABASE_SCHEMA}",
            "sslmode": "prefer",  # Default SSL mode for PostgreSQL
        }


# Example usage for future database implementations
def example_connection_usage() -> None:
    """Show how to use the database configuration.

    This function demonstrates different ways to access database
    configuration for various database libraries.
    """
    # For libraries that accept individual parameters
    conn_params = DatabaseConfig.get_connection_params()
    print(f"Connection parameters: {conn_params}")

    # For libraries that accept connection URLs
    conn_url = DatabaseConfig.get_connection_url()
    print(f"Connection URL: {conn_url}")

    # For schema-specific queries
    schema = DatabaseConfig.get_schema_name()
    print(f"Schema: {schema}")

    # For Alembic migrations
    alembic_config = DatabaseConfig.get_alembic_config()
    print(f"Alembic config: {alembic_config}")

    # For migration connection arguments
    migration_args = DatabaseConfig.get_migration_connection_args()
    print(f"Migration connection args: {migration_args}")


if __name__ == "__main__":
    example_connection_usage()
