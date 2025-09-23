import logging
from typing import Annotated, Iterator, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from src.core.database import create_session
from src.core.repositories.user_repository import UserRepository
from src.domain.users.models import User, UserPermission
from src.domain.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()
logger = logging.getLogger(__name__)


# --- FastAPI dependency factories & reusable parameter defaults ---
def get_db() -> Iterator[Session]:
    """Provide a database session for request handling and ensure cleanup.

    We intentionally avoid using the @contextmanager-wrapped get_session here
    because FastAPI expects a generator dependency that yields the resource.
    """
    session = create_session()
    try:
        yield session
    finally:
        session.close()


# Module-level Depends to satisfy flake8-bugbear B008 (no call in defaults)
DB_DEP = Depends(get_db)


def get_user_repo(db: Session = DB_DEP) -> Iterator[UserRepository]:
    """Provide a UserRepository tied to the current DB session."""
    try:
        repo = UserRepository(db)
        yield repo
    except Exception as e:
        logger.error(f"Failed to create UserRepository: {e}")
        raise


# Reusable dependency for endpoints
REPO_DEP = Depends(get_user_repo)

# Reusable Path/Query specs to satisfy flake8-bugbear B008
USER_ID_PATH = Path(..., ge=1)
PERMISSION_Q = Query(default=None, description="Filter by user permission")
OFFSET_Q = Query(0, ge=0)
LIMIT_Q = Query(100, ge=1, le=500)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    repo: UserRepository = REPO_DEP,
) -> UserRead:
    """Create a new user."""
    try:
        user = User(**payload.model_dump())
        created = repo.create(user)
        return UserRead.model_validate(created)
    except IntegrityError:
        # Likely duplicate email
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")


@router.get("/users", response_model=List[UserRead])
def list_users(
    permission: Optional[UserPermission] = PERMISSION_Q,
    offset: int = OFFSET_Q,
    limit: int = LIMIT_Q,
    repo: UserRepository = REPO_DEP,
) -> List[UserRead]:
    try:
        users = repo.list_users(permission=permission, offset=offset, limit=limit)
        return [UserRead.model_validate(u) for u in users]
    except Exception as e:
        logger.error(f"Error in list_users: {e}", exc_info=True)
        raise


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int = USER_ID_PATH,
    repo: UserRepository = REPO_DEP,
) -> UserRead:
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user)


@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(
    payload: Annotated[UserUpdate, Body()],
    user_id: int = USER_ID_PATH,
    repo: UserRepository = REPO_DEP,
) -> UserRead:
    try:
        updated = repo.update(user_id, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(updated)


@router.put("/users/{user_id}", response_model=UserRead)
def replace_user(
    payload: Annotated[UserCreate, Body()],
    user_id: int = USER_ID_PATH,
    repo: UserRepository = REPO_DEP,
) -> UserRead:
    """Replace a user with full data (idempotent-style update)."""
    try:
        updated = repo.update(user_id, payload.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(updated)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = USER_ID_PATH,
    repo: UserRepository = REPO_DEP,
) -> None:
    deleted = repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
