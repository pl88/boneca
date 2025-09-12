from datetime import datetime
from typing import Dict

from fastapi import APIRouter

from src.domain.users.schemas import UserCreate

router = APIRouter()


@router.get("/ping")
async def ping() -> Dict[str, str]:
    return {"response": f"pong {datetime.utcnow().isoformat()}"}
