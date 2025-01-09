from fastapi import FastAPI, Request, Response, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base  # 更新這行
from pydantic import BaseModel
from typing import Optional, List
# import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uuid import UUID, uuid4
import secrets
from fastapi.templating import Jinja2Templates
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware  # 改用 Starlette 的 session

# 資料庫設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # 這樣使用就不會有警告

# 資料模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    title = Column(String)
    body = Column(String)

# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class PostCreate(BaseModel):
    title: str
    body: str

# 建立資料庫表格
Base.metadata.create_all(bind=engine)

# FastAPI 應用程式
app = FastAPI()

# 加入 session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-here",  # 請更換為安全的密鑰
    session_cookie="blog_session"
)

# 設定模板
templates = Jinja2Templates(directory="templates")

# 依賴項
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由
@app.get("/", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).all()
    user = request.session.get("user")
    print(f'user={user} posts={posts}')
    r =  templates.TemplateResponse(
        "list.html",
        {"request": request, "posts": posts, "user": user}
    )
    template = templates.get_template("list.html")
    rendered_text = template.render(request=request, posts=posts, user=user)
    print(f'rendered_text={rendered_text}')
    return r


@app.get("/signup", response_class=HTMLResponse)
async def signup_ui(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=username, password=password, email=email)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def login_ui(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    request.session["user"] = {"username": username}
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/post/new", response_class=HTMLResponse)
async def new_post(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return templates.TemplateResponse("new_post.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def show_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(
        "show_post.html",
        {"request": request, "post": post}
    )

@app.post("/post")
async def create_post(
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_post = Post(username=user["username"], title=title, body=body)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

