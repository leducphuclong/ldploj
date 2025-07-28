import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This line allows alembic to find your app's modules
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Import your Pydantic settings
from backend.app.core.config import settings

# 2. Import your models' Base
# NOTE: Make sure this path is correct for your project structure
from backend.app.db.base import Base 

# 3. Import your models for autogenerate support
from backend.app.models import user, post

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Set the target_metadata for 'autogenerate' support
target_metadata = Base.metadata

# 5. Set the SQLAlchemy URL from your pydantic settings
db_url = settings.DATABASE_URL
if db_url and "postgresql+asyncpg" in db_url:
    db_url = db_url.replace("+asyncpg", "")

# NEW FIX: Escape percent signs for configparser
db_url = db_url.replace('%', '%%')

# We pass this modified URL to the Alembic config.
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()