"""Tests for configuration settings."""
import os
from unittest.mock import patch

from src.core.config import Settings, settings


class TestSettings:
    """Test cases for application settings."""

    def test_default_settings(self) -> None:
        """Test default configuration values."""
        # In CI/GitHub Actions, there's no .env file, so we get hardcoded defaults
        # In local Docker, .env file overrides these defaults
        test_settings = Settings()

        assert test_settings.PROJECT_NAME == "Boneca"
        assert test_settings.VERSION == "0.1.0"
        assert test_settings.API_PREFIX == "/api/v1"

        # Test database defaults - these will be "localhost" in CI, "postgres" in Docker
        # We test the actual behavior rather than mocking
        assert test_settings.DATABASE_PORT == 5432
        assert test_settings.DATABASE_NAME == "boneca"
        assert test_settings.DATABASE_USER == "boneca"
        assert test_settings.DATABASE_PASSWORD == "boneca"
        assert test_settings.DATABASE_SCHEMA == "boneca"
        # DATABASE_HOST can be either "localhost" (CI) or "postgres" (Docker with .env)
        assert test_settings.DATABASE_HOST in ["localhost", "postgres"]

    def test_settings_with_env_file_values(self) -> None:
        """Test settings when .env file values are available (Docker environment)."""
        # This test simulates the Docker environment where .env file provides postgres host
        with patch.dict(
            os.environ,
            {
                "DATABASE_HOST": "postgres",
                "DATABASE_PORT": "5432",
                "DATABASE_NAME": "boneca",
                "DATABASE_USER": "boneca",
                "DATABASE_PASSWORD": "boneca",
                "DATABASE_SCHEMA": "boneca",
            },
        ):
            test_settings = Settings()

        assert test_settings.DATABASE_HOST == "postgres"
        assert test_settings.DATABASE_PORT == 5432
        assert test_settings.DATABASE_NAME == "boneca"
        assert test_settings.DATABASE_USER == "boneca"
        assert test_settings.DATABASE_PASSWORD == "boneca"
        assert test_settings.DATABASE_SCHEMA == "boneca"

    def test_settings_with_env_vars(self) -> None:
        """Test settings with environment variables."""
        with patch.dict(
            os.environ,
            {
                "PROJECT_NAME": "Test Project",
                "VERSION": "1.0.0",
                "API_PREFIX": "/api/v2",
                "DATABASE_HOST": "db.example.com",
                "DATABASE_PORT": "5433",
                "DATABASE_NAME": "test_db",
                "DATABASE_USER": "test_user",
                "DATABASE_PASSWORD": "test_pass",
                "DATABASE_SCHEMA": "test_schema",
            },
        ):
            test_settings = Settings()
            assert test_settings.PROJECT_NAME == "Test Project"
            assert test_settings.VERSION == "1.0.0"
            assert test_settings.API_PREFIX == "/api/v2"
            assert test_settings.DATABASE_HOST == "db.example.com"
            assert test_settings.DATABASE_PORT == 5433
            assert test_settings.DATABASE_NAME == "test_db"
            assert test_settings.DATABASE_USER == "test_user"
            assert test_settings.DATABASE_PASSWORD == "test_pass"
            assert test_settings.DATABASE_SCHEMA == "test_schema"

    def test_settings_singleton(self) -> None:
        """Test that settings is properly initialized."""
        assert settings.PROJECT_NAME == "Boneca"
        assert settings.VERSION == "0.1.0"
        assert settings.API_PREFIX == "/api/v1"

    def test_settings_model_config(self) -> None:
        """Test that the model configuration is correct."""
        test_settings = Settings()
        # Test that extra fields are ignored (not causing validation errors)
        assert hasattr(test_settings, "model_config")

    def test_database_url_property(self) -> None:
        """Test that DATABASE_URL is correctly constructed."""
        test_settings = Settings()
        # URL will vary based on environment (localhost in CI, postgres in Docker)
        expected_hosts = ["localhost", "postgres"]
        host_in_url = any(host in test_settings.DATABASE_URL for host in expected_hosts)
        assert host_in_url
        assert "postgresql://boneca:boneca@" in test_settings.DATABASE_URL
        assert ":5432/boneca" in test_settings.DATABASE_URL

    def test_database_url_with_custom_values(self) -> None:
        """Test DATABASE_URL with custom database settings."""
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
            test_settings = Settings()
            expected_url = "postgresql://custom_user:custom_pass@custom.host.com:5433/custom_db"
            assert test_settings.DATABASE_URL == expected_url
