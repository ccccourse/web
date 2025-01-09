from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# FastAPI 初始化
app = FastAPI()

# 靜態文件與模板設置
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 資料庫設置
DATABASE_URL = "sqlite:///./blog.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 資料庫模型
class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

# 創建資料表
Base.metadata.create_all(bind=engine)

# 依賴項：獲取資料庫會話
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由
@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/article/create")
def create_article_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/article/create")
def create_article(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    new_article = Article(title=title, content=content)
    db.add(new_article)
    db.commit()
    return RedirectResponse("/", status_code=302)

@app.get("/article/{article_id}")
def read_article(request: Request, article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse("detail.html", {"request": request, "article": article})
