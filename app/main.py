from fastapi import FastAPI
from app.routers import auth, post, comment

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])

@app.get("/")
def root():
    return {"msg": "FastAPI Blog API running"}