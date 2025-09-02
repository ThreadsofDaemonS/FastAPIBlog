# routers/post.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.post import PostCreate, PostRead
from app.services.post import (
    create_post,
    get_posts_by_user,
    get_post,
    update_post,
    delete_post,
)
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PostRead)
async def create_post_view(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await create_post(user.id, post_in, db)

@router.get("/", response_model=list[PostRead])
async def get_my_posts(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    records = await get_posts_by_user(user.id, db)
    return [PostRead.model_validate(row) for row in records]

@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await get_post(post_id, user.id, db)