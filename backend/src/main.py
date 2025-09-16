"""Main application module.

This module initializes the FastAPI application and configures the main routes.
"""
from fastapi import FastAPI

from src.api.router import router as api_router
from src.core.config import settings

boneca = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_PREFIX}/docs",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

boneca.include_router(api_router, prefix=settings.API_PREFIX)


@boneca.get("/")
async def root() -> dict:
    """Get root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing the welcome message.
    """
    return {"message": "Hello Boneca users!"}
