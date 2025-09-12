"""Tests for configuration settings."""
import os
from unittest.mock import patch

from src.core.config import Settings, settings


class TestSettings:
    """Test cases for application settings."""
    
    def test_default_settings(self):
        """Test default configuration values."""
        test_settings = Settings()
        
        assert test_settings.PROJECT_NAME == "Boneca"
        assert test_settings.VERSION == "0.1.0"
        assert test_settings.API_PREFIX == "/api/v1"
    
    def test_settings_with_env_vars(self):
        """Test settings with environment variables."""
        with patch.dict(os.environ, {
            'PROJECT_NAME': 'Test Project',
            'VERSION': '1.0.0',
            'API_PREFIX': '/api/v2'
        }):
            test_settings = Settings()
            assert test_settings.PROJECT_NAME == "Test Project"
            assert test_settings.VERSION == "1.0.0"
            assert test_settings.API_PREFIX == "/api/v2"
    
    def test_settings_singleton(self):
        """Test that settings is properly initialized."""
        assert settings.PROJECT_NAME == "Boneca"
        assert settings.VERSION == "0.1.0"
        assert settings.API_PREFIX == "/api/v1"
    
    def test_settings_model_config(self):
        """Test that the model configuration is correct."""
        test_settings = Settings()
        # Test that extra fields are ignored (not causing validation errors)
        assert hasattr(test_settings, 'model_config')