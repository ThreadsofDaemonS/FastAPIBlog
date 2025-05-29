from pydantic import BaseModel, ConfigDict

class PostCreate(BaseModel):
    content: str
    auto_reply_enabled: bool = False
    reply_delay_sec: int = 0

class PostRead(BaseModel):
    id: int
    content: str
    is_blocked: bool
    auto_reply_enabled: bool
    reply_delay_sec: int

    model_config = ConfigDict(from_attributes=True)
