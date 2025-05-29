from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.schemas.post import PostCreate
from app.services.ai_moderation import is_text_toxic

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

async def get_posts_by_user(user_id: int, db: AsyncSession):
    result = await db.execute(Post.__table__.select().where(Post.user_id == user_id))
    return result.fetchall()
