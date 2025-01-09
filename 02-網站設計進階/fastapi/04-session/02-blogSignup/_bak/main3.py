from fastapi import FastAPI, Request, Response, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_sessions.frontends.implementations import SessionCookie
from fastapi_sessions.backends.implementations import InMemoryBackend
from uuid import UUID, uuid4
import secrets

# 資料庫設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

class SessionData(BaseModel):
    username: str

# 建立資料庫表格
Base.metadata.create_all(bind=engine)

# Session 管理
cookie_name = "blog_session"
cookie = SessionCookie(
    cookie_name=cookie_name,
    identifier="general_verifier",
    auto_error=True,
    secret_key="CHANGE_THIS_TO_A_REAL_SECRET_KEY",
    cookie_params={"httponly": True}
)
backend = InMemoryBackend[UUID, SessionData]()

# FastAPI 應用程式
app = FastAPI()

# 依賴項
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HTML 範本 (這裡簡化處理，實際應用建議使用 Jinja2 等範本引擎)
def render_template(template: str, **kwargs) -> str:
    # 這裡應該實作實際的範本渲染邏輯
    return f"<html><body>{template}</body></html>"

# 路由
@app.get("/", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).all()
    session_id = request.cookies.get(cookie_name)
    user = None
    if session_id:
        try:
            user_data = await backend.read(UUID(session_id))
            user = user_data
        except:
            pass
    return render_template("list.html", posts=posts, user=user)

@app.get("/signup", response_class=HTMLResponse)
async def signup_ui():
    return render_template("signup.html")

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
async def login_ui():
    return render_template("login.html")

@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    session_id = uuid4()
    await backend.create(session_id, SessionData(username=username))
    cookie.attach_to_response(response, session_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(cookie_name)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/post/new", response_class=HTMLResponse)
async def new_post(request: Request):
    session_id = request.cookies.get(cookie_name)
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return render_template("new_post.html")

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def show_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return render_template("show_post.html", post=post)

@app.post("/post")
async def create_post(
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db)
):
    session_id = request.cookies.get(cookie_name)
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        user_data = await backend.read(UUID(session_id))
        new_post = Post(username=user_data.username, title=title, body=body)
        db.add(new_post)
        db.commit()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except:
        raise HTTPException(status_code=401, detail="Invalid session")

