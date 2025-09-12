"""Application configuration module.

This module defines the application settings that can be configured
through environment variables or .env files.
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings model.

    Attributes:
        PROJECT_NAME: The name of the project.
        VERSION: The current version of the application.
        API_PREFIX: The prefix for all API endpoints.
    """

    PROJECT_NAME: str = "Boneca"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
