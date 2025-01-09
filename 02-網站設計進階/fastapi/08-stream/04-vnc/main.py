from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return HTMLResponse(content="<h1>VNC Client</h1><p>請使用 VNC 介面進行操作</p>", status_code=200)

@app.get("/vnc")
async def start_vnc():
    # 這裡可以處理開始 VNC 會話的邏輯
    return {"message": "VNC 會話已啟動"}
