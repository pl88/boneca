"""Health check endpoints module.

This module provides endpoints for health checking and monitoring the API service.
"""
from datetime import datetime
from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Check API health by returning a timestamp.

    Returns:
        Dict[str, str]: A dictionary with the current UTC timestamp.
    """
    return {"response": f"pong {datetime.utcnow().isoformat()}"}
