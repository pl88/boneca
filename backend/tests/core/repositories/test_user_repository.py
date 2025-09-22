"""Tests for User repository.

This module tests the UserRepository functionality with SQLModel.
"""
from unittest.mock import MagicMock, Mock

import pytest

from src.core.repositories.user_repository import UserRepository
from src.domain.users.models import User, UserPermission


class TestUserRepository:
    """Test cases for the UserRepository class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.repository = UserRepository(self.mock_session)

    def test_create_user(self):
        """Test creating a new user."""
        # Arrange
        user_data = User(
            first_name="John", last_name="Doe", email="john.doe@example.com", permissions=UserPermission.STUDENT
        )

        # Act
        result = self.repository.create(user_data)

        # Assert
        self.mock_session.add.assert_called_once_with(user_data)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(user_data)
        assert result == user_data

    def test_get_by_id(self):
        """Test getting a user by ID."""
        # Arrange
        user_id = 1
        expected_user = User(id=1, first_name="Jane", last_name="Smith", email="jane@example.com")
        self.mock_session.get.return_value = expected_user

        # Act
        result = self.repository.get_by_id(user_id)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        assert result == expected_user

    def test_get_by_id_not_found(self):
        """Test getting a user by ID when user doesn't exist."""
        # Arrange
        user_id = 999
        self.mock_session.get.return_value = None

        # Act
        result = self.repository.get_by_id(user_id)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        assert result is None

    def test_get_by_email(self):
        """Test getting a user by email."""
        # Arrange
        email = "test@example.com"
        expected_user = User(id=1, first_name="Test", last_name="User", email=email)

        # Mock the exec chain
        mock_result = Mock()
        mock_result.first.return_value = expected_user
        self.mock_session.exec.return_value = mock_result

        # Act
        result = self.repository.get_by_email(email)

        # Assert
        self.mock_session.exec.assert_called_once()
        assert result == expected_user

    def test_list_users_no_filter(self):
        """Test listing users without filters."""
        # Arrange
        expected_users = [
            User(id=1, first_name="User1", last_name="Test", email="user1@example.com"),
            User(id=2, first_name="User2", last_name="Test", email="user2@example.com"),
        ]

        mock_result = Mock()
        mock_result.all.return_value = expected_users
        self.mock_session.exec.return_value = mock_result

        # Act
        result = self.repository.list_users()

        # Assert
        self.mock_session.exec.assert_called_once()
        assert result == expected_users

    def test_list_users_with_permission_filter(self):
        """Test listing users filtered by permission."""
        # Arrange
        permission = UserPermission.ADMIN
        expected_users = [
            User(id=1, first_name="Admin", last_name="User", email="admin@example.com", permissions=permission)
        ]

        mock_result = Mock()
        mock_result.all.return_value = expected_users
        self.mock_session.exec.return_value = mock_result

        # Act
        result = self.repository.list_users(permission=permission)

        # Assert
        self.mock_session.exec.assert_called_once()
        assert result == expected_users

    def test_update_user_success(self):
        """Test updating a user successfully."""
        # Arrange
        user_id = 1
        existing_user = User(id=1, first_name="Old", last_name="Name", email="old@example.com")
        update_data = {"first_name": "New", "email": "new@example.com"}

        self.mock_session.get.return_value = existing_user

        # Act
        result = self.repository.update(user_id, update_data)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(existing_user)

        assert existing_user.first_name == "New"
        assert existing_user.email == "new@example.com"
        assert result == existing_user

    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist."""
        # Arrange
        user_id = 999
        update_data = {"first_name": "New"}

        self.mock_session.get.return_value = None

        # Act
        result = self.repository.update(user_id, update_data)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        self.mock_session.commit.assert_not_called()
        assert result is None

    def test_delete_user_success(self):
        """Test deleting a user successfully."""
        # Arrange
        user_id = 1
        existing_user = User(id=1, first_name="To", last_name="Delete", email="delete@example.com")

        self.mock_session.get.return_value = existing_user

        # Act
        result = self.repository.delete(user_id)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        self.mock_session.delete.assert_called_once_with(existing_user)
        self.mock_session.commit.assert_called_once()
        assert result is True

    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist."""
        # Arrange
        user_id = 999
        self.mock_session.get.return_value = None

        # Act
        result = self.repository.delete(user_id)

        # Assert
        self.mock_session.get.assert_called_once_with(User, user_id)
        self.mock_session.delete.assert_not_called()
        assert result is False

    def test_count_by_permission(self):
        """Test counting users by permission level."""
        # Arrange
        permission = UserPermission.INSTRUCTOR
        mock_users = [Mock(), Mock(), Mock()]  # 3 instructors

        mock_result = Mock()
        mock_result.all.return_value = mock_users
        self.mock_session.exec.return_value = mock_result

        # Act
        result = self.repository.count_by_permission(permission)

        # Assert
        self.mock_session.exec.assert_called_once()
        assert result == 3

    def test_search_by_name(self):
        """Test searching users by name."""
        # Arrange
        search_term = "John"
        expected_users = [
            User(id=1, first_name="John", last_name="Doe", email="john@example.com"),
            User(id=2, first_name="Jane", last_name="Johnson", email="jane@example.com"),
        ]

        mock_result = Mock()
        mock_result.all.return_value = expected_users
        self.mock_session.exec.return_value = mock_result

        # Act
        result = self.repository.search_by_name(search_term)

        # Assert
        self.mock_session.exec.assert_called_once()
        assert result == expected_users
