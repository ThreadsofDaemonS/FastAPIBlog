from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.services.ai_moderation import is_text_toxic
from app.services.auto_reply import schedule_auto_reply

async def create_comment(user_id: int, data: CommentCreate, db: AsyncSession):
    is_blocked = is_text_toxic(data.content)

    comment = Comment(
        user_id=user_id,
        post_id=data.post_id,
        content=data.content,
        is_blocked=is_blocked,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    if not is_blocked:
        await schedule_auto_reply(comment, db)

    return comment

async def get_comments_by_post(post_id: int, db: AsyncSession):
    result = await db.execute(Comment.__table__.select().where(Comment.post_id == post_id))
    return result.fetchall()
