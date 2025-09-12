"""Tests for the base repository."""
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel

from src.core.exceptions import EntityNotFoundError
from src.core.repositories.base import BaseRepository


class TestEntity(BaseModel):
    """Test entity for repository tests."""

    id: UUID
    name: str


class TestRepository(BaseRepository[TestEntity]):
    """Test repository implementation."""

    async def connect(self) -> None:
        """Connect to the repository."""
        pass

    async def disconnect(self) -> None:
        """Disconnect from the repository."""
        pass

    async def get(self, id: UUID) -> TestEntity:
        """Get an entity."""
        raise EntityNotFoundError("test", str(id))

    async def list(self, *, filters: dict | None = None, offset: int = 0, limit: int = 100) -> list[TestEntity]:
        """List entities."""
        return []

    async def create(self, entity: TestEntity) -> TestEntity:
        """Create an entity."""
        return entity

    async def update(self, id: UUID, entity: TestEntity) -> TestEntity:
        """Update an entity."""
        return entity

    async def delete(self, id: UUID) -> None:
        """Delete an entity."""
        pass


async def test_repository_context_manager():
    """Test repository context manager protocol."""
    repo = TestRepository()
    async with repo:
        assert isinstance(repo, BaseRepository)


async def test_repository_get_not_found():
    """Test repository get method with non-existent entity."""
    repo = TestRepository()
    with pytest.raises(EntityNotFoundError) as exc_info:
        await repo.get(uuid4())
    assert "Test with ID" in str(exc_info.value)


async def test_repository_list_empty():
    """Test repository list method with empty repository."""
    repo = TestRepository()
    entities = await repo.list()
    assert entities == []
