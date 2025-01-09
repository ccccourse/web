from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_sessions import SessionManager, sessionmaker
from fastapi_sessions.frontends.cookie import CookieBackend
from fastapi_sessions.state import Session
from pydantic import BaseModel
from passlib.context import CryptContext

# 假設的用戶資料庫
fake_users_db = {}

# 密碼加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI 應用
app = FastAPI()

# 會話管理配置
SESSION_SECRET_KEY = "a4c5c345c35c465b28c5cc28e838e32a"  # 用來加密 Session 的密鑰
session_backend = CookieBackend(secret_key=SESSION_SECRET_KEY, cookie_name="session_id", cookie_max_age=3600)
session_manager = SessionManager(backend=session_backend)

# Pydantic 模型
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# 密碼加密
def hash_password(password: str):
    return pwd_context.hash(password)

# 驗證密碼
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 註冊用戶
@app.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
    return {"msg": "User created successfully"}

# 登入並建立會話
@app.post("/login")
async def login(request: Request, user: User, session: Session = Depends(session_manager)):
    stored_user = fake_users_db.get(user.username)
    if stored_user is None or not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session["username"] = user.username  # 設定會話中的用戶名
    return JSONResponse(content={"msg": "Login successful"}, status_code=200)

# 受保護路由
@app.get("/protected")
async def protected_route(request: Request, session: Session = Depends(session_manager)):
    username = session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"msg": f"Welcome {username}"}

# 登出並清除會話
@app.post("/logout")
async def logout(request: Request, session: Session = Depends(session_manager)):
    session.clear()  # 清除會話
    return {"msg": "Logged out successfully"}
