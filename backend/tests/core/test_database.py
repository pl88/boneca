"""Tests for database configuration utilities."""
import os
from unittest.mock import patch

from src.core.database import DatabaseConfig


class TestDatabaseConfig:
    """Test cases for database configuration utilities."""

    def test_get_connection_params_default(self) -> None:
        """Test getting connection parameters with default settings."""
        params = DatabaseConfig.get_connection_params()

        # Host will be "localhost" in CI, "postgres" in Docker environment
        assert params["host"] in ["localhost", "postgres"]
        assert params["port"] == 5432
        assert params["database"] == "boneca"
        assert params["user"] == "boneca"
        assert params["password"] == "boneca"
        assert params["options"] == "-c search_path=boneca"

    def test_get_connection_url_default(self) -> None:
        """Test getting connection URL with default settings."""
        url = DatabaseConfig.get_connection_url()

        # URL will vary based on environment (localhost in CI, postgres in Docker)
        expected_urls = [
            "postgresql://boneca:boneca@localhost:5432/boneca",
            "postgresql://boneca:boneca@postgres:5432/boneca",
        ]
        assert url in expected_urls

    def test_get_schema_name_default(self) -> None:
        """Test getting schema name with default settings."""
        schema = DatabaseConfig.get_schema_name()
        assert schema == "boneca"

    def test_get_connection_params_with_env_vars(self) -> None:
        """Test connection parameters with custom environment variables."""
        with patch.dict(
            os.environ,
            {
                "DATABASE_HOST": "db.example.com",
                "DATABASE_PORT": "5433",
                "DATABASE_NAME": "test_db",
                "DATABASE_USER": "test_user",
                "DATABASE_PASSWORD": "test_pass",
                "DATABASE_SCHEMA": "test_schema",
            },
        ):
            # Import and create a new Settings instance to pick up env vars
            from src.core.config import Settings
            from src.core.database import DatabaseConfig

            # Create new instance that will read current env vars
            test_settings = Settings()

            # Patch the settings module to use our test instance
            with patch("src.core.database.settings", test_settings):
                params = DatabaseConfig.get_connection_params()
                assert params["host"] == "db.example.com"
                assert params["port"] == 5433
                assert params["database"] == "test_db"
                assert params["user"] == "test_user"
                assert params["password"] == "test_pass"
                assert params["options"] == "-c search_path=test_schema"

    def test_get_connection_url_with_env_vars(self) -> None:
        """Test connection URL with custom environment variables."""
        with patch.dict(
            os.environ,
            {
                "DATABASE_HOST": "custom.host.com",
                "DATABASE_PORT": "5433",
                "DATABASE_NAME": "custom_db",
                "DATABASE_USER": "custom_user",
                "DATABASE_PASSWORD": "custom_pass",
            },
        ):
            # Import and create a new Settings instance to pick up env vars
            from src.core.config import Settings
            from src.core.database import DatabaseConfig

            # Create new instance that will read current env vars
            test_settings = Settings()

            # Patch the settings module to use our test instance
            with patch("src.core.database.settings", test_settings):
                url = DatabaseConfig.get_connection_url()
                expected = "postgresql://custom_user:custom_pass@custom.host.com:5433/custom_db"
                assert url == expected
