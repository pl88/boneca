"""Tests for users endpoints."""
from src.api.v1.users import create_user, get_user, list_users
from src.domain.users.schemas import UserCreate


class TestUsersEndpoints:
    """Test cases for users endpoints."""

    def test_create_user_function_exists(self):
        """Test that create_user function exists and is callable."""
        assert callable(create_user)

    async def test_create_user_returns_welcome_message(self):
        """Test creating a user returns welcome message."""
        user_data = UserCreate(name="Test User")
        response = await create_user(user_data)

        assert isinstance(response, dict)
        assert "message" in response
        assert "Test User" in response["message"]
        assert response["message"] == "Welcome in Boneca dear Test User"

    def test_list_users_function_exists(self):
        """Test that list_users function exists and is callable."""
        assert callable(list_users)

    async def test_list_users_returns_empty_list(self):
        """Test listing users returns empty list."""
        response = await list_users()

        assert isinstance(response, dict)
        assert "users" in response
        assert isinstance(response["users"], list)
        assert response["users"] == []

    def test_get_user_function_exists(self):
        """Test that get_user function exists and is callable."""
        assert callable(get_user)

    async def test_get_user_returns_user_info(self):
        """Test getting a specific user returns user info."""
        user_id = 123
        response = await get_user(user_id)

        assert isinstance(response, dict)
        assert "user_id" in response
        assert "message" in response
        assert response["user_id"] == str(user_id)
        assert response["message"] == "User details would be here"
