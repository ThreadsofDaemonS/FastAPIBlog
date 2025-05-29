from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False)
    auto_reply_enabled = Column(Boolean, default=False)
    reply_delay_sec = Column(Integer, default=0)

    user = relationship("User", back_populates="posts")
