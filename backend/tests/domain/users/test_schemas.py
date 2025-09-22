"""Tests for user schemas."""
import pytest
from pydantic import ValidationError

from src.domain.users.models import UserPermission
from src.domain.users.schemas import UserCreate


class TestUserSchemas:
    """Test cases for user data models and schemas."""

    def test_user_create_valid(self) -> None:
        """Test creating a valid UserCreate instance."""
        user = UserCreate(first_name="John", last_name="Doe", email="john.doe@example.com")

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        # default permission
        assert user.permissions == UserPermission.STUDENT

    def test_user_create_missing_required_fields(self) -> None:
        """Test UserCreate validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate()  # type: ignore[call-arg]

        # Check that first_name, last_name, and email are required
        errors = exc_info.value.errors()
        fields = {e["loc"][0] for e in errors}
        assert {"first_name", "last_name", "email"} <= fields

    def test_user_create_empty_first_name_invalid(self) -> None:
        """Test UserCreate with empty first_name is invalid (min length 1)."""
        with pytest.raises(ValidationError):
            UserCreate(first_name="", last_name="Doe", email="john.doe@example.com")

    def test_user_create_serialization(self) -> None:
        """Test UserCreate model serialization."""
        user = UserCreate(first_name="Test", last_name="User", email="test.user@example.com")
        user_dict = user.model_dump()

        assert user_dict == {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "permissions": "student",
        }
        assert isinstance(user_dict, dict)
