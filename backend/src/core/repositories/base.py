"""Base repository interface and abstract implementations."""
from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager, Generic, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(Generic[T], AsyncContextManager["BaseRepository[T]"], ABC):
    """Abstract base repository interface.

    This class defines the standard interface for all repositories in the application.
    It uses generic type T to represent the entity type being stored.

    All concrete repositories should inherit from this class and implement its methods.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the repository.

        This method should establish any necessary connections or initialize resources.
        It is called automatically when using the repository as an async context manager.

        Raises:
            ConnectionError: If connection fails
        """
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the repository.

        This method should clean up any resources and close connections.
        It is called automatically when exiting the async context manager.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> T:
        """Retrieve an entity by its ID.

        Args:
            id: The unique identifier of the entity

        Returns:
            The entity if found

        Raises:
            EntityNotFoundError: If the entity doesn't exist
            RepositoryError: If there's an error accessing the repository
        """
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        *,
        filters: Optional[dict[str, Any]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """List entities with optional filtering and pagination.

        Args:
            filters: Optional dictionary of field-value pairs to filter by
            offset: Number of records to skip (for pagination)
            limit: Maximum number of records to return (for pagination)

        Returns:
            List of entities matching the criteria

        Raises:
            RepositoryError: If there's an error accessing the repository
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity.

        Args:
            entity: The entity to create

        Returns:
            The created entity (with any generated fields like ID)

        Raises:
            EntityConflictError: If an entity with conflicting unique fields exists
            ValidationError: If the entity fails validation
            RepositoryError: If there's an error accessing the repository
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, entity: T) -> T:
        """Update an existing entity.

        Args:
            id: The unique identifier of the entity to update
            entity: The updated entity data

        Returns:
            The updated entity

        Raises:
            EntityNotFoundError: If the entity doesn't exist
            EntityConflictError: If the update would create conflicts
            ValidationError: If the entity fails validation
            RepositoryError: If there's an error accessing the repository
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """Delete an entity by its ID.

        Args:
            id: The unique identifier of the entity to delete

        Raises:
            EntityNotFoundError: If the entity doesn't exist
            RepositoryError: If there's an error accessing the repository
        """
        raise NotImplementedError

    async def __aenter__(self) -> "BaseRepository[T]":
        """Enter the async context manager.

        Connects to the repository when entering the context.

        Returns:
            The repository instance

        Raises:
            ConnectionError: If connection fails
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context manager.

        Disconnects from the repository when exiting the context.
        """
        await self.disconnect()
