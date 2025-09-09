# tests/conftest.py
# Purpose: async test fixtures using httpx.AsyncClient + ASGITransport,
#          DB session override, isolated transaction per test, and JWT helper.
#          + full DB cleanup after the whole test session.

import asyncio
import uuid
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.main import app
from app.core.db import get_db, AsyncSessionLocal, engine, Base
from app.core.security import create_access_token

# Ensure models are imported so their metadata is registered on Base
from app.models import user as _user_model  # noqa: F401
from app.models import post as _post_model  # noqa: F401
from app.models import comment as _comment_model  # noqa: F401


@pytest.fixture(scope="session")
def event_loop():
    """Session-scoped event loop to match session fixtures."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_test_environment():
    """
    Ensure DB connectivity and make sure tables exist for tests.
    If Alembic already ran, create_all() is a no-op.
    """
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Если хочется — можно дропать всё после сессии:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_test_environment) -> AsyncIterator[AsyncSession]:
    """
    Provide a single transaction per test and roll it back after the test.
    """
    async with AsyncSessionLocal() as session:
        trans = await session.begin()
        try:
            yield session
        finally:
            # Сервисные функции могут коммитить — тогда транзакция будет закрыта.
            if trans.is_active:
                await trans.rollback()
            await session.close()


@pytest_asyncio.fixture
async def override_get_db(db_session: AsyncSession):
    """
    Override FastAPI dependency to inject the test AsyncSession.
    """
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    try:
        yield
    finally:
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(override_get_db) -> AsyncIterator[AsyncClient]:
    """
    Async HTTP client with app lifespan (startup/shutdown) enabled.
    httpx>=0.28 → use ASGITransport(app=app).
    """
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """
    Create a unique test user via service layer.
    Генерируем УНИКАЛЬНЫЙ email на вызов фикстуры (сервис коммитит).
    """
    from app.services.auth import create_user
    from app.schemas.user import UserCreate

    unique = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        # username — если поле есть в схеме; по логам модель может быть без него.
        username=f"u_{unique}",
        email=f"test_{unique}_user@example.com",
        password="password123",
    )
    user = await create_user(user_data, db_session)
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user) -> dict:
    """
    Issue a valid JWT for the created test user.
    В токен кладём email, потому что у модели нет поля username.
    """
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}


# -----------------------------
# Автоматическая очистка БД
# -----------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_after_tests():
    """
    После завершения ВСЕЙ сессии тестов подчистить данные:
    TRUNCATE users, posts, comments RESTART IDENTITY CASCADE.
    """
    # до тестов — ничего
    yield
    # после тестов — чистим
    async with engine.begin() as conn:
        # порядок не важен из-за CASCADE; RESTART IDENTITY сбрасывает序ции ID
        await conn.execute(
            text("TRUNCATE TABLE comments, posts, users RESTART IDENTITY CASCADE")
        )
