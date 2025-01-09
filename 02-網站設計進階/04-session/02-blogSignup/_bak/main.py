from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.sessions import SessionMiddleware, Session
from sqlite3 import connect

import os

# 初始化 FastAPI 應用
app = FastAPI()

# 添加 session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# 初始化 Jinja2 模板引擎
templates = Jinja2Templates(directory="templates")

# 連接 SQLite 數據庫
def get_db():
    db_path = "blog.db"
    if not os.path.exists(db_path):
        conn = connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, title TEXT, body TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT)")
        conn.commit()
    return connect(db_path)

# 數據庫操作
def sqlcmd(sql, params=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql, params)
    db.commit()
    return cursor.fetchall()

# 頁面渲染函數
async def render_template(request: Request, template_name: str, **kwargs):
    return templates.TemplateResponse(template_name, {"request": request, **kwargs})

# 註冊頁面
@app.get("/signup", response_class=HTMLResponse)
async def signup_ui(request: Request):
    return await render_template(request, "signup.html")

@app.post("/signup")
async def signup(request: Request, username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    user_check = sqlcmd("SELECT id FROM users WHERE username=?", (username,))
    if user_check:
        return {"message": "Username already exists"}
    sqlcmd("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    return RedirectResponse(url="/", status_code=303)

# 登入頁面
@app.get("/login", response_class=HTMLResponse)
async def login_ui(request: Request):
    return await render_template(request, "login.html")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    user = sqlcmd("SELECT id, username, password FROM users WHERE username=?", (username,))
    if user and user[0][2] == password:  # 密碼匹配
        request.session["user"] = username
        return RedirectResponse(url="/", status_code=303)
    else:
        return {"message": "Invalid username or password"}

# 登出
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# 文章頁面
@app.get("/post/new", response_class=HTMLResponse)
async def add_post(request: Request):
    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    return await render_template(request, "new_post.html")

@app.get("/post/{id}", response_class=HTMLResponse)
async def show_post(request: Request, id: int):
    post = sqlcmd("SELECT id, username, title, body FROM posts WHERE id=?", (id,))
    if post:
        return await render_template(request, "show_post.html", post=post[0])
    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/post")
async def create_post(request: Request, title: str = Form(...), body: str = Form(...)):
    if "user" not in request.session:
        raise HTTPException(status_code=403, detail="Not logged in")
    username = request.session["user"]
    sqlcmd("INSERT INTO posts (username, title, body) VALUES (?, ?, ?)", (username, title, body))
    return RedirectResponse(url="/", status_code=303)

# 首頁，列出所有文章
@app.get("/", response_class=HTMLResponse)
async def list_posts(request: Request):
    posts = sqlcmd("SELECT id, username, title, body FROM posts")
    return await render_template(request, "list.html", posts=posts)
