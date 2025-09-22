"""Error-path tests for users API endpoints.

Covers conflict (409) and not found (404) branches, and dependency cleanup.
"""
from collections.abc import Iterator
from typing import Any, Generator, Optional, Tuple, cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from src.main import boneca as app


class ErrorUserRepo:
    """Repository stub that can be configured to raise or return values."""

    def __init__(self) -> None:
        """Initialize flags controlling behavior for tests."""
        self.raise_on_create = False
        self.raise_on_update = False
        self.update_returns_none = False
        self.delete_returns_false = False

    # Signature mirrors real repo methods used by the router
    def create(self, user):  # noqa: ANN001 - test helper
        if self.raise_on_create:
            raise IntegrityError("conflict", params=None, orig=Exception("orig"))
        return user

    def list_users(self, *args: object, **kwargs: object) -> list[dict]:  # test helper types
        return []

    def get_by_id(self, user_id: int) -> None:  # test helper types
        return None

    def update(self, user_id: int, user_data: dict) -> dict | None:  # test helper types
        if self.raise_on_update:
            raise IntegrityError("conflict", params=None, orig=Exception("orig"))
        if self.update_returns_none:
            return None
        return {"id": user_id, **user_data}

    def delete(self, user_id: int) -> bool:
        return not self.delete_returns_false


@pytest.fixture()
def client_and_repo() -> Iterator[Tuple[TestClient, ErrorUserRepo]]:
    from src.api.v1.users import get_user_repo

    repo = ErrorUserRepo()

    def override_get_user_repo() -> Iterator[ErrorUserRepo]:
        yield repo

    app.dependency_overrides[get_user_repo] = override_get_user_repo
    client = TestClient(app)
    try:
        yield client, repo
    finally:
        app.dependency_overrides.clear()


def test_create_user_conflict(client_and_repo: Tuple[TestClient, ErrorUserRepo]) -> None:
    client, repo = client_and_repo
    repo.raise_on_create = True

    r = client.post(
        "/api/v1/users",
        json={"first_name": "A", "last_name": "B", "email": "a@b.com", "permissions": "student"},
    )
    assert r.status_code == 409


def test_update_user_conflict_and_not_found(client_and_repo: Tuple[TestClient, ErrorUserRepo]) -> None:
    client, repo = client_and_repo

    # Conflict on patch
    repo.raise_on_update = True
    r = client.patch("/api/v1/users/1", json={"email": "dup@example.com"})
    assert r.status_code == 409

    # Not found on patch (update returns None)
    repo.raise_on_update = False
    repo.update_returns_none = True
    r2 = client.patch("/api/v1/users/1", json={"first_name": "X"})
    assert r2.status_code == 404


def test_replace_user_conflict(client_and_repo: Tuple[TestClient, ErrorUserRepo]) -> None:
    client, repo = client_and_repo
    repo.raise_on_update = True

    r = client.put(
        "/api/v1/users/1",
        json={"first_name": "A", "last_name": "B", "email": "a@b.com", "permissions": "student"},
    )
    assert r.status_code == 409


def test_delete_user_not_found(client_and_repo: Tuple[TestClient, ErrorUserRepo]) -> None:
    client, repo = client_and_repo
    repo.delete_returns_false = True

    r = client.delete("/api/v1/users/123")
    assert r.status_code == 404


def test_get_db_dependency_closes_session(monkeypatch: Any) -> None:
    # Arrange a dummy session to verify close() is called in finally
    class DummySession:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:  # pragma: no cover - trivial
            self.closed = True

    from src.api.v1 import users as users_module

    dummy = DummySession()
    # Patch create_session imported in users module scope
    monkeypatch.setattr(users_module, "create_session", lambda: dummy)

    # Act
    gen = users_module.get_db()
    got = next(gen)
    assert got is dummy
    assert dummy.closed is False
    cast(Generator, gen).close()  # trigger finally with proper typing

    # Assert
    assert dummy.closed is True
