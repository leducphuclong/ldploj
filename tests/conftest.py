# tests/conftest.py

import pytest_asyncio
from typing import AsyncGenerator

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# --- UPDATED IMPORT PATHS ---
from backend.app.main import app
from backend.app.db.base import Base
from backend.app.api import deps
from backend.app.core.config import Settings

# Create a new settings instance for testing that reads from .env.test
test_settings = Settings(_env_file=".env.test")

# Create a new async engine and session for the test database
test_engine = create_async_engine(test_settings.DATABASE_URL)
TestAsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """
    Fixture to create and drop the test database tables for the entire test session.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to provide a database session for a single test function.
    """
    async with TestAsyncSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to create an AsyncClient for making requests to the app.
    This client will use the test database.
    """
    # Dependency override: whenever get_db is called in the app,
    # it will use our test db_session instead.
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[deps.get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    
    # Clean up the override after the test
    del app.dependency_overrides[deps.get_db]