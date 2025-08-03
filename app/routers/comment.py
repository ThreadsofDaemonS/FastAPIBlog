from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment import create_comment, get_comments_by_post

def get_current_user_id():
    return 1

router = APIRouter()

@router.post("/", response_model=CommentRead)
async def create_comment_view(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await create_comment(user_id, comment_in, db)

@router.get("/post/{post_id}", response_model=list[CommentRead])
async def get_post_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    records = await get_comments_by_post(post_id, db)
    return [CommentRead.model_validate(row) for row in records]
