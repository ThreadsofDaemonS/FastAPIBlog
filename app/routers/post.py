from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.post import PostCreate, PostRead
from app.services.post import create_post, get_posts_by_user


def get_current_user_id():
    return 1

router = APIRouter()

@router.post("/", response_model=PostRead)
async def create_post_view(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await create_post(user_id, post_in, db)

@router.get("/", response_model=list[PostRead])
async def get_my_posts(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    records = await get_posts_by_user(user_id, db)
    return [PostRead.model_validate(row) for row in records]
