"""Tests for user schemas."""
import pytest
from pydantic import ValidationError

from src.domain.users.schemas import UserCreate


class TestUserSchemas:
    """Test cases for user data models and schemas."""

    def test_user_create_valid(self):
        """Test creating a valid UserCreate instance."""
        user_data = {"name": "John Doe"}
        user = UserCreate(**user_data)

        assert user.name == "John Doe"
        assert isinstance(user.name, str)

    def test_user_create_missing_name(self):
        """Test UserCreate validation with missing name."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate()

        # Check that name field is required
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert "name" in errors[0]["loc"]

    def test_user_create_empty_name(self):
        """Test UserCreate with empty name."""
        user = UserCreate(name="")
        assert user.name == ""

    def test_user_create_serialization(self):
        """Test UserCreate model serialization."""
        user = UserCreate(name="Test User")
        user_dict = user.model_dump()

        assert user_dict == {"name": "Test User"}
        assert isinstance(user_dict, dict)
