from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional

app = FastAPI()

# 設置 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key_here")

# 模擬的用戶數據
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "1234"
    }
}

# 用戶登錄檢查函數
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

# 檢查 session 是否已登錄
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user

@app.post("/login")
def login(username: str, password: str, request: Request):
    user = authenticate_user(username, password)
    if user:
        request.session["user"] = user["username"]  # 保存用戶名到 session
        return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.get("/secure-endpoint")
def secure_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}

@app.post("/logout")
def logout(request: Request):
    request.session.pop("user", None)  # 移除 session 中的用戶
    return {"message": "Logout successful"}
