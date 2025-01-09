from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

# 資料庫設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料模型
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

# Pydantic 模型
class PostCreate(BaseModel):
    title: str
    body: str

# 建立資料庫表格
Base.metadata.create_all(bind=engine)

# FastAPI 應用程式
app = FastAPI()

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
async def list_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("list.html", {"request": request, "posts": posts})

@app.get("/post/new", response_class=HTMLResponse)
async def new_post(request: Request):
    return templates.TemplateResponse("new_post.html", {"request": request})

@app.post("/post")
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db)
):
    new_post = Post(title=title, body=body)  # 預設用 guest
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def show_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("show_post.html", {"request": request, "post": post})
