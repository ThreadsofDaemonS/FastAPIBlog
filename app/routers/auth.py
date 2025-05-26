from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.services.auth import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(user_in.email, db)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = await create_user(user_in, db)
    return user

@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(user_in.email, db)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
