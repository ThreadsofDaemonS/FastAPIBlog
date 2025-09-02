from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.schemas.post import PostCreate
from app.services.ai_moderation import is_text_toxic
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException

async def create_post(user_id: int, data: PostCreate, db: AsyncSession):
    is_blocked = is_text_toxic(data.content)

    post = Post(
        user_id=user_id,
        content=data.content,
        is_blocked=is_blocked,
        auto_reply_enabled=data.auto_reply_enabled,
        reply_delay_sec=data.reply_delay_sec,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_posts_by_user(user_id: int, db: AsyncSession) -> list[Post]:
    result = await db.execute(Post.__table__.select().where(Post.user_id == user_id))
    return result.fetchall()

async def get_post(post_id: int, user_id: int, db: AsyncSession) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id, Post.user_id == user_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

async def update_post(post_id: int, user_id: int, data: PostCreate, db: AsyncSession):
    post = await get_post(post_id, user_id, db)
    post.content = data.content
    post.auto_reply_enabled = data.auto_reply_enabled
    post.reply_delay_sec = data.reply_delay_sec
    post.is_blocked = is_text_toxic(data.content)
    await db.commit()
    await db.refresh(post)
    return post

async def delete_post(post_id: int, user_id: int, db: AsyncSession):
    post = await get_post(post_id, user_id, db)
    await db.delete(post)
    await db.commit()