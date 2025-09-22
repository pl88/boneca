"""Tests for users API CRUD endpoints using dependency overrides."""
from collections.abc import Iterator
from typing import Optional

import pytest
from fastapi.testclient import TestClient

from src.domain.users.models import User, UserPermission
from src.domain.users.schemas import UserCreate, UserUpdate
from src.main import boneca as app


class FakeUserRepo:
    """In-memory fake UserRepository for testing without DB."""

    def __init__(self) -> None:
        """Initialize the in-memory storage and id counter."""
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create(self, user: User) -> User:
        user.id = self._next_id
        self._next_id += 1
        # emulate storage copy
        self._users[user.id] = User(**user.model_dump())
        return self._users[user.id]

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def list_users(
        self,
        *,
        permission: Optional[UserPermission] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[User]:
        users = list(self._users.values())
        if permission:
            users = [u for u in users if u.permissions == permission]
        return users[offset : offset + limit]

    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self._users.get(user_id)
        if not user:
            return None
        for k, v in user_data.items():
            if hasattr(user, k):
                setattr(user, k, v)
        self._users[user_id] = User(**user.model_dump())
        return self._users[user_id]

    def delete(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None


@pytest.fixture()
def client_with_fake_repo() -> Iterator[TestClient]:
    from src.api.v1.users import get_user_repo

    fake_repo = FakeUserRepo()

    def override_get_user_repo() -> Iterator[FakeUserRepo]:
        yield fake_repo

    app.dependency_overrides[get_user_repo] = override_get_user_repo
    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.clear()


def test_create_and_get_user(client_with_fake_repo: TestClient) -> None:
    client = client_with_fake_repo
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "permissions": "student",
    }

    # Create
    r = client.post("/api/v1/users", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] == 1
    assert data["email"] == payload["email"]

    # Get by id
    r2 = client.get("/api/v1/users/1")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["first_name"] == "Jane"


def test_list_and_filter_users(client_with_fake_repo: TestClient) -> None:
    client = client_with_fake_repo

    # Seed two users with different permissions
    client.post(
        "/api/v1/users",
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "permissions": "instructor",
        },
    )
    client.post(
        "/api/v1/users",
        json={
            "first_name": "Alice",
            "last_name": "Jones",
            "email": "alice.jones@example.com",
            "permissions": "student",
        },
    )

    r = client.get("/api/v1/users")
    assert r.status_code == 200
    all_users = r.json()
    assert len(all_users) >= 2

    r2 = client.get("/api/v1/users", params={"permission": "instructor"})
    assert r2.status_code == 200
    only_instructors = r2.json()
    assert all(u["permissions"] == "instructor" for u in only_instructors)


def test_update_and_delete_user(client_with_fake_repo: TestClient) -> None:
    client = client_with_fake_repo
    # Create user
    r = client.post(
        "/api/v1/users",
        json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob.brown@example.com",
        },
    )
    assert r.status_code == 201

    # Patch update
    r2 = client.patch("/api/v1/users/1", json={"first_name": "Bobby"})
    assert r2.status_code == 200
    assert r2.json()["first_name"] == "Bobby"

    # Put replace
    r3 = client.put(
        "/api/v1/users/1",
        json={
            "first_name": "Robert",
            "last_name": "Brown",
            "email": "robert.brown@example.com",
            "permissions": "viewer",
        },
    )
    assert r3.status_code == 200
    assert r3.json()["email"] == "robert.brown@example.com"
    assert r3.json()["permissions"] == "viewer"

    # Delete
    r4 = client.delete("/api/v1/users/1")
    assert r4.status_code == 204

    # Not found after delete
    r5 = client.get("/api/v1/users/1")
    assert r5.status_code == 404
