"""Core exceptions module for the application."""
from typing import Any, Optional


class BonecaError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class RepositoryError(BonecaError):
    """Base exception for repository-related errors."""

    pass


class EntityNotFoundError(RepositoryError):
    """Raised when an entity is not found in the repository."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            entity_type: Type of entity that was not found (e.g., "user", "class")
            entity_id: ID of the entity that was not found
        """
        super().__init__(
            f"{entity_type.title()} with ID {entity_id} not found",
            {"entity_type": entity_type, "entity_id": entity_id},
        )


class EntityConflictError(RepositoryError):
    """Raised when there's a conflict creating or updating an entity."""

    def __init__(self, entity_type: str, field: str, value: Any) -> None:
        """Initialize the exception.

        Args:
            entity_type: Type of entity with the conflict (e.g., "user", "class")
            field: Field that caused the conflict (e.g., "email", "username")
            value: Value that caused the conflict
        """
        super().__init__(
            f"{entity_type.title()} with {field}={value} already exists",
            {"entity_type": entity_type, "field": field, "value": value},
        )


class ValidationError(BonecaError):
    """Raised when entity validation fails."""

    def __init__(self, entity_type: str, errors: dict[str, Any]) -> None:
        """Initialize the exception.

        Args:
            entity_type: Type of entity that failed validation
            errors: Dictionary of validation errors
        """
        super().__init__(
            f"Validation failed for {entity_type}",
            {"entity_type": entity_type, "errors": errors},
        )


class ConnectionError(RepositoryError):
    """Raised when repository connection fails."""

    def __init__(self, repository_type: str, details: Optional[dict[str, Any]] = None) -> None:
        """Initialize the exception.

        Args:
            repository_type: Type of repository that failed to connect
            details: Optional dictionary with connection error details
        """
        super().__init__(
            f"Failed to connect to {repository_type} repository",
            {"repository_type": repository_type, **(details or {})},
        )


class ConfigurationError(BonecaError):
    """Raised when there's a configuration-related error."""

    def __init__(self, config_key: str, message: str) -> None:
        """Initialize the exception.

        Args:
            config_key: Configuration key that caused the error
            message: Error message explaining the issue
        """
        super().__init__(
            f"Configuration error for {config_key}: {message}",
            {"config_key": config_key},
        )
