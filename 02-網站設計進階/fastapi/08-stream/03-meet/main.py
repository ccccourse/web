from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 儲存連接的 WebSocket 客戶端
clients = []

@app.get("/", response_class=HTMLResponse)
async def get_root():
    with open("static/index.html", "r") as file:
        return HTMLResponse(file.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 廣播給所有其他客戶端
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
