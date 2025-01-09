from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os

app = FastAPI()

# 設定資料庫文件名稱
DB_NAME = "fts_example.db"


# 設置靜態檔案目錄，提供前端資源
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化資料庫
@app.on_event("startup")
async def startup_event():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 創建 FTS 表格
    cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS articles USING FTS5(id, title, content)")
    # 插入數據
    cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (1, "Python Basics", "Learn the basics of Python programming."))
    cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (2, "SQLite FTS", "Full-text search with SQLite FTS is powerful and easy to use."))
    cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (3, "FastAPI Guide", "Build APIs quickly using FastAPI."))
    conn.commit()
    conn.close()

# 插入範例資料
@app.post("/add/")
async def add_article(id: int, title: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (id, title, content))
    conn.commit()
    conn.close()
    return {"message": "Document added"}

# 搜尋功能
@app.get("/search/")
async def search_article(query: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM articles WHERE articles MATCH ?", (query,))
    results = cursor.fetchall()
    conn.close()
    return {"results": [{"id": r[0], "title": r[1], "content": r[2]} for r in results]}

# 供前端使用的 HTML 網頁
@app.get("/", response_class=HTMLResponse)
async def get_search_page():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
