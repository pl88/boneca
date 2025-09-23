"""Database session management for SQLModel.

This module provides database session creation and management utilities.
"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from src.core.config import settings

# Create the engine - this would typically be a singleton
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL logging in development
    connect_args={"options": f"-csearch_path={settings.DATABASE_SCHEMA}"},
)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a database session.

    This is a context manager that provides a database session
    and ensures it's properly closed after use.

    Usage:
        with get_session() as session:
            user_repo = UserRepository(session)
            user = user_repo.get_by_id(1)

    Yields:
        SQLModel Session instance
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def create_session() -> Session:
    """Create a new database session.

    Note: Caller is responsible for closing the session.
    Consider using get_session() context manager instead.

    Returns:
        SQLModel Session instance
    """
    return Session(engine)
