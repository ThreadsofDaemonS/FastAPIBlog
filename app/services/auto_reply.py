import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.services.ai_moderation import generate_reply

async def schedule_auto_reply(comment: Comment, db: AsyncSession):
    post = await db.get(Post, comment.post_id)
    if not post or not post.auto_reply_enabled:
        return

    if comment.user_id == post.user_id:     ### DON'T FORGET ABOUT THIS
        return

    await asyncio.sleep(post.reply_delay_sec or 1)

    reply_text = generate_reply(post.content, comment.content)

    reply = Comment(
        user_id=comment.user_id,
        post_id=post.id,
        content=reply_text,
        is_blocked=False,
    )
    db.add(reply)
    await db.commit()
