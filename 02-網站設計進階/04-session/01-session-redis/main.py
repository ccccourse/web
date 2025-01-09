from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis.asyncio as redis
import uuid
import json

app = FastAPI()

# Redis 連接
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class LoginRequest(BaseModel):
    username: str
    password: str

# Session 管理函數
async def create_session(username):
    session_id = str(uuid.uuid4())
    session_data = json.dumps({"username": username})
    await redis_client.setex(f"session:{session_id}", 3600, session_data)
    return session_id

async def verify_session(session_id):
    session_data = await redis_client.get(f"session:{session_id}")
    if session_data:
        return json.loads(session_data)
    return None

# 登入端點
@app.post("/login")
async def login(data: LoginRequest):
    if data.username == "admin" and data.password == "password":
        session_id = await create_session(data.username)
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# 受保護路由的依賴
async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    session_data = await verify_session(session_id)
    if not session_data:
        raise HTTPException(status_code=403, detail="Invalid or expired session")
    
    return session_data['username']

# 受保護的路由
@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Welcome, {username}!"}

# 登出端點
@app.post("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        await redis_client.delete(f"session:{session_id}")
    
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("session_id")
    return response