"""SQLModel-based repository for User operations.

This repository provides data access operations for User entities using SQLModel.
"""
from typing import Optional

from sqlalchemy import select
from sqlmodel import Session

from src.domain.users.models import User, UserPermission


class UserRepository:
    """Repository for User entity operations using SQLModel.
    
    Provides CRUD operations and custom queries for User entities.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: SQLModel/SQLAlchemy session for database operations
        """
        self.session = session

    def create(self, user: User) -> User:
        """Create a new user.
        
        Args:
            user: User instance to create
            
        Returns:
            The created user with assigned ID
            
        Raises:
            IntegrityError: If email already exists or other constraint violations
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            User instance if found, None otherwise
        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address.
        
        Args:
            email: The user's email address
            
        Returns:
            User instance if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def list_users(
        self,
        *,
        permission: Optional[UserPermission] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """List users with optional filtering.
        
        Args:
            permission: Optional permission level to filter by
            offset: Number of records to skip (pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of users matching the criteria
        """
        statement = select(User)
        
        if permission:
            statement = statement.where(User.permissions == permission)
            
        statement = statement.offset(offset).limit(limit)
        
        return list(self.session.exec(statement).all())

    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update a user.
        
        Args:
            user_id: The user's ID
            user_data: Dictionary of fields to update
            
        Returns:
            Updated user instance if found, None otherwise
            
        Raises:
            IntegrityError: If update violates constraints (e.g., duplicate email)
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
            
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
                
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """Delete a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            True if user was deleted, False if not found
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
            
        self.session.delete(user)
        self.session.commit()
        return True

    def count_by_permission(self, permission: UserPermission) -> int:
        """Count users by permission level.
        
        Args:
            permission: The permission level to count
            
        Returns:
            Number of users with the specified permission
        """
        statement = select(User).where(User.permissions == permission)
        return len(list(self.session.exec(statement).all()))

    def search_by_name(self, search_term: str) -> list[User]:
        """Search users by first or last name.
        
        Args:
            search_term: Term to search for in names
            
        Returns:
            List of users whose first or last name contains the search term
        """
        search_pattern = f"%{search_term}%"
        statement = select(User).where(
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern))
        )
        return list(self.session.exec(statement).all())