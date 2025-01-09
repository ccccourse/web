from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI()

posts = []
# 假設的資料
"""
posts = [
    {"id": 0, "title": "aaa", "body": "aaaaa"},
    {"id": 1, "title": "bbb", "body": "bbbbb"}
]
"""

# 定義資料模型
class Post(BaseModel):
    title: str
    body: str

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/list")
async def list_posts():
    return JSONResponse(content=posts)

@app.get("/post/{id}")
async def show_post(id: int):
    if id < 0 or id >= len(posts):
        raise HTTPException(status_code=404, detail="Invalid post id")
    return JSONResponse(content=posts[id])

@app.post("/post")
async def create_post(post: Post):
    new_post = post.dict()
    new_post["id"] = len(posts)
    posts.append(new_post)
    return {"message": "success", "post": new_post}
