"""Tests for core exceptions."""
import pytest

from src.core.exceptions import (
    BonecaError,
    ConfigurationError,
    ConnectionError,
    EntityConflictError,
    EntityNotFoundError,
    RepositoryError,
    ValidationError,
)


def test_boneca_error():
    """Test BonecaError base class."""
    error = BonecaError("Test error", {"detail": "test"})
    assert str(error) == "Test error"
    assert error.details == {"detail": "test"}


def test_repository_error():
    """Test RepositoryError base class."""
    error = RepositoryError("Test error", {"detail": "test"})
    assert str(error) == "Test error"
    assert error.details == {"detail": "test"}
    assert isinstance(error, BonecaError)


def test_entity_not_found_error():
    """Test EntityNotFoundError."""
    error = EntityNotFoundError("user", "123")
    assert "User" in str(error)  # Note: gets capitalized in message
    assert "123" in str(error)
    assert isinstance(error, RepositoryError)


def test_entity_conflict_error():
    """Test EntityConflictError."""
    error = EntityConflictError("user", "email", "test@example.com")
    assert "User" in str(error)  # Note: gets capitalized in message
    assert "email" in str(error)
    assert "test@example.com" in str(error)
    assert isinstance(error, RepositoryError)


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError("user", {"field": "error"})
    assert "user" in str(error)
    assert isinstance(error, BonecaError)
    assert error.details["errors"] == {"field": "error"}


def test_connection_error():
    """Test ConnectionError."""
    error = ConnectionError("postgres", {"host": "localhost"})
    assert "postgres" in str(error)
    assert isinstance(error, RepositoryError)
    assert "host" in error.details


def test_configuration_error():
    """Test ConfigurationError."""
    error = ConfigurationError("DATABASE_URL", "Missing required value")
    assert "DATABASE_URL" in str(error)
    assert isinstance(error, BonecaError)
    assert error.details["config_key"] == "DATABASE_URL"
