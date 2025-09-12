"""Tests for healthcheck endpoints."""
from datetime import datetime

from src.api.v1.healthcheck import ping


class TestHealthCheck:
    """Test cases for health check endpoints."""

    def test_ping_function_exists(self) -> None:
        """Test that the ping function exists and is callable."""
        assert callable(ping)

    async def test_ping_endpoint_returns_dict(self) -> None:
        """Test the ping endpoint returns correct response format."""
        response = await ping()

        assert isinstance(response, dict)
        assert "response" in response
        assert response["response"].startswith("pong ")

    async def test_ping_timestamp_format(self) -> None:
        """Test that ping returns valid ISO timestamp."""
        response = await ping()
        timestamp_part = response["response"].replace("pong ", "")

        # This should not raise an exception if it's a valid ISO format
        parsed_time = datetime.fromisoformat(timestamp_part.replace("Z", "+00:00"))
        assert isinstance(parsed_time, datetime)
