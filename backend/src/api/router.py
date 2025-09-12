"""API router configuration module.

This module sets up the main API router and includes all sub-routers
for different API versions and endpoints.
"""
from fastapi import APIRouter

from src.api.v1 import healthcheck

router = APIRouter()

router.include_router(healthcheck.router, tags=["health"])
