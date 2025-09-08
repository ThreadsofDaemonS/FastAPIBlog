import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.core.db import get_db, Base
from app.models.user import User  # Приклад для створення тестового користувача
from decouple import Config, RepositoryEnv
from unittest.mock import patch

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


@pytest.fixture(scope="session")
def event_loop():
    """Створити подієвий цикл для тестової сесії."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_test_db():
    """Підготовка бази даних для тестування (один раз за сесію)."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def db_session(setup_test_db):
    """Чиста сесія бази даних для кожного тесту."""
    async with TestingSessionLocal() as session:
        # Почати транзакцію
        transaction = await session.begin()
        yield session
        # Відкотити транзакцію для очищення
        await transaction.rollback()


@pytest.fixture
async def client(db_session):
    """Тестовий клієнт із перевизначеною залежністю бази даних."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    """Фікстура для створення тестового користувача."""
    user = User(email="test@example.com", hashed_password="hashed_password")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def authenticated_client(client, test_user):
    """Фікстура для аутентифікованого клієнта."""
    # Симуляція авторизації
    token = "mocked_jwt_token"
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def mock_google_ai():
    """Фікстура для мокування Google AI API."""
    with patch("services.ai_moderation.client.models.generate_content") as mock:
        yield mock