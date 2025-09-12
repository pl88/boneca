from typing import List

from fastapi import APIRouter

from src.domain.users.schemas import UserCreate

router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate) -> dict[str, str]:
    return {"message": f"Welcome in Boneca dear {user.name}"}


@router.get("/users")
async def list_users() -> dict[str, List[dict]]:
    # This is a placeholder implementation
    return {"users": []}


@router.get("/users/{user_id}")
async def get_user(user_id: int) -> dict[str, str]:
    # This is a placeholder implementation
    return {"user_id": str(user_id), "message": "User details would be here"}
