"""Tests for the main API router."""
from fastapi import APIRouter

from src.api.router import router
from src.api.v1 import healthcheck, users


class TestAPIRouter:
    """Test cases for the main API router."""
    
    def test_router_is_api_router_instance(self):
        """Test that the router is an APIRouter instance."""
        assert isinstance(router, APIRouter)
        
    def test_router_has_routes(self):
        """Test that the router has been configured with routes."""
        # The router should have routes from included sub-routers
        assert len(router.routes) > 0
        
    def test_healthcheck_router_imported(self):
        """Test that healthcheck router is properly imported."""
        assert hasattr(healthcheck, 'router')
        assert isinstance(healthcheck.router, APIRouter)
        
    def test_users_router_imported(self):
        """Test that users router is properly imported."""
        assert hasattr(users, 'router')
        assert isinstance(users.router, APIRouter)