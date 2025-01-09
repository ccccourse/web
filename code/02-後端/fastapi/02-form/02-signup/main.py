from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import hashlib

# 初始化 FastAPI 應用
app = FastAPI()

# 模擬 "資料庫"，實際應該使用真實資料庫
fake_db = {}

# 設定 HTML 模板
templates = Jinja2Templates(directory="templates")

# 讓 FastAPI 支援靜態檔案 (如 CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 首頁顯示註冊登入選單
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 註冊頁面
@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# 註冊處理
@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    # 檢查帳號是否已經註冊
    if username in fake_db:
        raise HTTPException(status_code=400, detail="帳號已經註冊")
    
    # 密碼加密 (簡單的 hash，實際應用中應使用更安全的方式)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # 儲存帳號和密碼
    fake_db[username] = hashed_password
    return RedirectResponse(url="/login", status_code=303)


# 登入頁面
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 登入處理
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # 檢查帳號是否存在
    if username not in fake_db:
        raise HTTPException(status_code=400, detail="帳號不存在")
    
    # 檢查密碼是否正確
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if fake_db[username] != hashed_password:
        raise HTTPException(status_code=400, detail="密碼錯誤")

    return {"message": f"登入成功，歡迎 {username}!"}
