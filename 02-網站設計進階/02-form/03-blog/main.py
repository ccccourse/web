from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# 模擬資料
posts = [{"id": 0, "title": "aaa", "body": "aaaaa"}, {"id": 1, "title": "bbb", "body": "bbbbb"}]

# FastAPI 應用程式
app = FastAPI()

# 設定模板
templates = Jinja2Templates(directory="templates")

# 路由
@app.get("/", response_class=HTMLResponse)
async def list_posts(request: Request):
    return templates.TemplateResponse("list.html", {"request": request, "posts": posts})

@app.get("/post/new", response_class=HTMLResponse)
async def new_post(request: Request):
    return templates.TemplateResponse("new_post.html", {"request": request})

@app.post("/post")
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
):
    new_post = {"id":len(posts), "title":title, "body":body}
    posts.append(new_post)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def show_post(request: Request, post_id: int):
    post = posts[post_id]
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("show_post.html", {"request": request, "post": post})
