# main.py

from fastapi import FastAPI
from app.routers import auth, post, comment, analytics

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])