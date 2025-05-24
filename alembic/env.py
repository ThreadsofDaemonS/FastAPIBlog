from sqlalchemy import pool
from alembic import context

from decouple import config as env_config
import sys
import os

# Add app/ to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import Base, User  # TODO: імпортуй всі моделі тут

# Build DATABASE_URL from .env
DATABASE_URL = (
    f"postgresql+asyncpg://{env_config('POSTGRES_USER')}:{env_config('POSTGRES_PASSWORD')}"
    f"@{env_config('POSTGRES_HOST')}:{env_config('POSTGRES_PORT')}/{env_config('POSTGRES_DB')}"
)

print(f"[ALEMBIC] Using DATABASE_URL: {DATABASE_URL}")

# Alembic config setup
config = context.config
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncEngine
    import asyncio

    engine: AsyncEngine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())