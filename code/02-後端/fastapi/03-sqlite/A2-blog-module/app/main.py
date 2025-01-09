from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.crud import create_article, get_all_articles, get_article_by_id

# FastAPI 初始化
app = FastAPI()

# 靜態文件與模板設置
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="templates")

# 初始化資料庫
init_db()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    articles = get_all_articles(db)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/article/create")
def create_article_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/article/create")
def create_article_route(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    create_article(db, title, content)
    return RedirectResponse("/", status_code=302)

@app.get("/article/{article_id}")
def read_article(request: Request, article_id: int, db: Session = Depends(get_db)):
    article = get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse("detail.html", {"request": request, "article": article})
