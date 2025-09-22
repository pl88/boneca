"""Tests for user domain models.

This module tests the SQLModel User model and related components.
"""
import pytest
from src.domain.users.models import User, UserPermission


class TestUserModel:
    """Test cases for the User SQLModel."""

    def test_user_model_creation(self):
        """Test creating a User instance with valid data."""
        user = User(
            first_name="John",
            last_name="Doe", 
            email="john.doe@example.com",
            permissions=UserPermission.STUDENT
        )
        
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.permissions == UserPermission.STUDENT
        assert user.id is None  # ID is set by database

    def test_user_model_default_permissions(self):
        """Test that default permission is STUDENT."""
        user = User(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com"
        )
        
        assert user.permissions == UserPermission.STUDENT

    def test_user_permission_enum_values(self):
        """Test UserPermission enum has expected values."""
        assert UserPermission.ADMIN.value == "admin"
        assert UserPermission.INSTRUCTOR.value == "instructor" 
        assert UserPermission.STUDENT.value == "student"
        assert UserPermission.VIEWER.value == "viewer"

    def test_user_model_with_all_permissions(self):
        """Test creating users with different permission levels."""
        permissions = [
            UserPermission.ADMIN,
            UserPermission.INSTRUCTOR,
            UserPermission.STUDENT,
            UserPermission.VIEWER
        ]
        
        for permission in permissions:
            user = User(
                first_name="Test",
                last_name="User",
                email=f"test.{permission.value}@example.com",
                permissions=permission
            )
            assert user.permissions == permission

    def test_user_model_table_name(self):
        """Test that the table name is set correctly."""
        assert User.__tablename__ == "users"