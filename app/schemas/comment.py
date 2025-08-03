from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentRead(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    is_blocked: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
