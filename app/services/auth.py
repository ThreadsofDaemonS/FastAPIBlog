# services\auth.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.models.user import User

async def create_user(user_in: UserCreate, db: AsyncSession):
    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_all_users(db: AsyncSession):
    from sqlalchemy.future import select
    result = await db.execute(select(User))
    return result.scalars().all()

