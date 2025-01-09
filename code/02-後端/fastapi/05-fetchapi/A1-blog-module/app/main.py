from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.crud import create_article, get_all_articles, get_article_by_id

# FastAPI 初始化
app = FastAPI()

# CORS 設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 修改為特定域名以加強安全性
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 靜態文件設置
app.mount("/static", StaticFiles(directory="../static"), name="static")

# 初始化資料庫
init_db()

@app.get("/articles")
def read_articles(db: Session = Depends(get_db)):
    return get_all_articles(db)

@app.post("/articles")
def create_article_route(article: dict, db: Session = Depends(get_db)):
    title = article.get("title")
    content = article.get("content")
    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    return create_article(db, title, content)

@app.get("/articles/{article_id}")
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
