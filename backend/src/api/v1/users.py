from fastapi import APIRouter
from src.domain.users.schemas import UserCreate

router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate):
    return {"message": f"Welcome in Boneca dear {user.name}"}
