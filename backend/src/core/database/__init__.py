"""Database package compatibility shim.

This package exposes conveniences from the sibling module ``src.core.database``
(the file ``src/core/database.py``) while also providing the ``session``
submodule from this directory. This allows imports like::

    from src.core.database import DatabaseConfig
    from src.core.database import example_connection_usage
    from src.core.database.session import create_session

to work together even though a module file and a package share the same name.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, cast

# Dynamically load the sibling module file src/core/database.py under a
# different module name and re-export needed symbols here for compatibility.
_module_path = Path(__file__).resolve().parent.parent / "database.py"
_spec = importlib.util.spec_from_file_location("src.core._database_module", _module_path)
if _spec and _spec.loader:  # pragma: no cover - trivial import wiring
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    # Expose a settings attribute and proxy through to the sibling module
    from src.core.config import settings as _settings

    settings = _settings

    class DatabaseConfig:  # proxy
        """Proxy around the real DatabaseConfig syncing the settings object."""

        @staticmethod
        def get_connection_params() -> dict[str, str | int]:
            """Return DB connection params using current settings."""
            _mod.settings = settings  # type: ignore[attr-defined]
            return cast(dict[str, str | int], _mod.DatabaseConfig.get_connection_params())

        @staticmethod
        def get_connection_url() -> str:
            """Return DB connection URL using current settings."""
            _mod.settings = settings  # type: ignore[attr-defined]
            return cast(str, _mod.DatabaseConfig.get_connection_url())

        @staticmethod
        def get_schema_name() -> str:
            """Return DB schema name using current settings."""
            _mod.settings = settings  # type: ignore[attr-defined]
            return cast(str, _mod.DatabaseConfig.get_schema_name())

        @staticmethod
        def get_alembic_config() -> dict[str, Any]:
            """Return Alembic configuration using current settings."""
            _mod.settings = settings  # type: ignore[attr-defined]
            return cast(dict[str, Any], _mod.DatabaseConfig.get_alembic_config())

        @staticmethod
        def get_migration_connection_args() -> dict[str, Any]:
            """Return migration connection args using current settings."""
            _mod.settings = settings  # type: ignore[attr-defined]
            return cast(dict[str, Any], _mod.DatabaseConfig.get_migration_connection_args())

    def example_connection_usage() -> None:
        """Run the example connection usage with current settings."""
        _mod.settings = settings  # type: ignore[attr-defined]
        _mod.example_connection_usage()

else:  # pragma: no cover - defensive
    raise ImportError("Failed to load sibling module src/core/database.py")

__all__ = ["DatabaseConfig", "example_connection_usage", "settings"]
