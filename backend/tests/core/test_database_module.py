"""Tests for src/core/database.py utility functions to increase coverage."""
from typing import Any, Dict, List

from src.core.database import DatabaseConfig, example_connection_usage


def test_database_config_getters_return_values() -> None:
    params = DatabaseConfig.get_connection_params()
    assert "host" in params and "database" in params and "options" in params

    url = DatabaseConfig.get_connection_url()
    assert isinstance(url, str) and url.startswith("postgresql")

    schema = DatabaseConfig.get_schema_name()
    assert isinstance(schema, str) and schema

    alembic = DatabaseConfig.get_alembic_config()
    assert isinstance(alembic, dict) and "sqlalchemy.url" in alembic

    mig_args = DatabaseConfig.get_migration_connection_args()
    assert mig_args.get("options") and mig_args.get("sslmode")


def test_example_connection_usage_runs(monkeypatch: Any) -> None:
    # Prevent actual print to keep test output clean
    printed: List[str] = []

    def fake_print(*args: object, **kwargs: Dict[str, Any]) -> None:  # pragma: no cover - trivial
        printed.append("ok")

    monkeypatch.setattr("builtins.print", fake_print)
    example_connection_usage()
    # Should have attempted to print several lines
    assert printed  # at least one print occurred
