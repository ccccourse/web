from fastapi import FastAPI, Depends, Form, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import BaseUser, BaseUserCreate, BaseUserUpdate
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

# 設定 SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 用戶模型
class User(Base, BaseUser):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)

# 用戶創建與更新
class UserCreate(BaseUserCreate):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseUserUpdate):
    username: str
    full_name: str

class UserDB(User, BaseUser):
    pass

# 創建資料庫
Base.metadata.create_all(bind=engine)

# 使用者資料庫
def get_user_db():
    db = SessionLocal()
    try:
        # 使用 SQLAlchemyUserDatabase
        yield SQLAlchemyUserDatabase(UserDB, db)
    finally:
        db.close()

# JWT 認證策略
SECRET = "SECRET_KEY"
jwt_strategy = JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# FastAPI Users 配置
fastapi_users = FastAPIUsers[User, int](
    get_user_db,
    [jwt_strategy],
)

app = FastAPI()

# 設定 Jinja2 模板
templates = Jinja2Templates(directory="templates")

# 創建首頁路由
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 註冊頁面
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 註冊功能
@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user_create = UserCreate(username=username, email=email, password=password)
    user_db = await fastapi_users.create_user(user_create)
    if user_db:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=400, detail="註冊失敗")

# 登入頁面
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 登入功能
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await fastapi_users.get_user_manager().get_user(username)
    if user and await fastapi_users.get_user_manager().verify_password(password, user.password):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=401, detail="登入失敗")
