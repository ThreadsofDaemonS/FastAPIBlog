import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.core.db import get_db, Base
from app.models.user import User  # Приклад для створення тестового користувача
from decouple import Config, RepositoryEnv
from unittest.mock import patch
from app.core.security import hash_password, create_access_token

# Завантаження змінних середовища з .env.test
env_config = Config(RepositoryEnv(".env.test"))

# Отримання TEST_DATABASE_URL
TEST_DATABASE_URL = env_config(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://test_user:test_password@localhost:5433/test_blogdb"
)

if not TEST_DATABASE_URL:
    raise Exception("❌ TEST_DATABASE_URL is not set or is empty!")

print(f"🔍 [TESTS] Using database: {TEST_DATABASE_URL}")

# Створення двигуна для тестової бази даних
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,  # Встановіть True для дебагінгу SQL-запитів
    future=True
)

# Конфігурація сесії SQLAlchemy
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def setup_test_db():
    """Підготовка бази даних для тестування (один раз за сесію)."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_test_db):
    """Чиста сесія бази даних для кожного тесту."""
    # Create a fresh session for each test
    async with TestingSessionLocal() as session:
        yield session
        # After test - manually clean up all tables
        await session.rollback()
        # Delete all data from tables
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest_asyncio.fixture
async def client(db_session):
    """Тестовий клієнт із перевизначеною залежністю бази даних."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Фікстура з даними тестового користувача."""
    return {
        "email": "test@example.com",
        "password": "password123"
    }


@pytest_asyncio.fixture
async def test_user(db_session, test_user_data):
    """Фікстура для створення тестового користувача."""
    user = User(
        email=test_user_data["email"], 
        hashed_password=hash_password(test_user_data["password"])
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def authenticated_user(client, test_user, test_user_data):
    """Фікстура для аутентифікованого користувача."""
    # Створити JWT токен для тестового користувача
    access_token = create_access_token(data={"sub": test_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    return {
        "user": test_user,
        "user_data": test_user_data,
        "headers": headers,
        "token": access_token
    }


@pytest.fixture
def mock_google_ai():
    """Фікстура для мокування Google AI API."""
    with patch("app.services.ai_moderation.client.models.generate_content") as mock:
        yield mock