"""Application configuration module.

This module defines the application settings that can be configured
through environment variables or .env files.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings model.

    Attributes:
        PROJECT_NAME: The name of the project.
        VERSION: The current version of the application.
        API_PREFIX: The prefix for all API endpoints.

        # Database settings
        DATABASE_HOST: The PostgreSQL host.
        DATABASE_PORT: The PostgreSQL port.
        DATABASE_NAME: The PostgreSQL database name.
        DATABASE_USER: The PostgreSQL username.
        DATABASE_PASSWORD: The PostgreSQL password.
        DATABASE_SCHEMA: The PostgreSQL schema name.
        DATABASE_URL: Complete database connection URL (auto-constructed if not provided).
    """

    PROJECT_NAME: str = "Boneca"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    # Database configuration
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "boneca"
    DATABASE_USER: str = "boneca"
    DATABASE_PASSWORD: str = "boneca"
    DATABASE_SCHEMA: str = "boneca"

    @property
    def DATABASE_URL(self) -> str:
        """Construct the database URL from components."""
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
