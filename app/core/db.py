from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from decouple import config
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = config("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
