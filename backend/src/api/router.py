from fastapi import APIRouter

from src.api.v1 import healthcheck, users

router = APIRouter()

router.include_router(healthcheck.router, tags=["health"])
router.include_router(users.router, tags=["users"])
