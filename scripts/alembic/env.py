import asyncio
import importlib
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine


# Add the project root to the Python path for module resolution
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from src.config.config import settings  # noqa: E402
from src.db.base import Base  # noqa: E402

# Alembic Config object, provides access to .ini file values
config = context.config

# Set up Python logging using Alembic config file if available
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def import_all_models():
    """
    Automatically discover and import all models from all apps in the src/app directory.

    This ensures all models are registered with SQLAlchemy Base for Alembic's autogenerate support.
    Handles both 'models' directories and single 'models.py' files in each app.
    """
    app_dir = settings.APP_DIR

    if not app_dir.exists():
        print(f"Warning: App directory not found at {app_dir}")
        return

    # Iterate through all subdirectories in src/app
    for app_path in app_dir.iterdir():
        if not app_path.is_dir() or app_path.name.startswith("_"):
            continue

        app_name = app_path.name
        models_module_name = f"src.app.{app_name}.models"
        try:
            importlib.import_module(models_module_name)
            print(f"Imported: {models_module_name}")
        except ImportError as e:
            print(f"Warning: Could not import {models_module_name}: {e}")
        except Exception as e:
            print(f"Error importing models from {app_path.name}: {e}")


# Import all models before setting target_metadata for Alembic
import_all_models()

# Set target_metadata for Alembic's autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Configures the context with just a database URL, without creating an Engine.
    Calls to context.execute() emit the given SQL string to the script output.
    """
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    Run migrations using a provided database connection.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Creates an async Engine and associates a connection with the context.
    """
    connectable = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Entry point: choose offline or online migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
