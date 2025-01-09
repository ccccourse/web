from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware  # 新增這行
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os

# 創建 FastAPI 應用
app = FastAPI()

# 添加 SessionMiddleware
# 注意：在生產環境中，SECRET_KEY 應該是安全的隨機值
app.add_middleware(
    SessionMiddleware, 
    secret_key="your-secret-key-here"  # 請使用安全的隨機密鑰
)

# 允許跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 設定
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile',
        'response_type': 'code',
    },
)

# 用戶模型
class User(BaseModel):
    id: Optional[str] = None
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

# 模擬用戶數據庫
users_db = {}

# OAuth2 token 提取器
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Google 登入路由
@app.get('/login/google')
async def google_login(request: Request):
    # 使用正確的重定向 URI
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Google 回調處理
@app.get('/auth/google')
async def google_auth(request: Request):
    try:
        # 交換 authorization code 獲取 token
        token = await oauth.google.authorize_access_token(request)
        
        # 從 Google 獲取用戶信息
        user_info = await oauth.google.parse_id_token(request, token)
        
        # 創建或更新用戶
        user = User(
            id=user_info.get('sub'),
            email=user_info.get('email'),
            name=user_info.get('name'),
            picture=user_info.get('picture')
        )
        
        # 存儲或更新用戶到數據庫
        users_db[user.id] = user.dict()
        
        # 生成自定義 token 或重定向
        return {
            "message": "登入成功",
            "user": user.dict(),
            "access_token": token['access_token']
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 其他路由保持不變...
# 獲取當前用戶信息
@app.get('/users/me')
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 在實際應用中，這裡應該驗證 token
    for user_id, user_data in users_db.items():
        if user_data.get('id'):
            return user_data
    
    raise HTTPException(status_code=401, detail="未找到用戶")

# 登出路由
@app.get('/logout')
async def logout():
    # 清理用戶 session 或 token
    return {"message": "成功登出"}

# 公開路由
@app.get('/public')
async def public_endpoint():
    return {"message": "這是公開路由"}

# 主頁
@app.get('/')
async def home():
    return {
        "message": "歡迎使用 Google OAuth 登入",
        "login_url": "/login/google"
    }