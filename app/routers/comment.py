# routers/comment.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment import create_comment, get_comments_by_post
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CommentRead)
async def create_comment_view(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await create_comment(user.id, comment_in, db)

@router.get("/post/{post_id}", response_model=list[CommentRead])
async def get_post_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    records = await get_comments_by_post(post_id, db)
    return [CommentRead.model_validate(row) for row in records]