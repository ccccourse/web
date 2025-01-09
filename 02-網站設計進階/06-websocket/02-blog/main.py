from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

# 模擬資料
posts = [{"id": 0, "title": "aaa", "body": "aaaaa"}, {"id": 1, "title": "bbb", "body": "bbbbb"}]

# Mount the static directory
app.mount("/static", StaticFiles(directory="./static"), name="static")

# WebSocket 管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: str):
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass  # Handle client disconnection gracefully

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 伺服端點，處理連線、訊息接收與廣播。
    """
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")
            msg = json.loads(message)
            response = {}

            if msg.get("type") == "list":
                response = {"type": "list", "posts": posts}
            elif msg.get("type") == "show":
                post = posts[msg.get("post", {}).get("id")]
                response = {"type": "show", "post": post}
            elif msg.get("type") == "create":
                post = msg.get("post")
                post["created_at"] = "now"  # Replace with real timestamp if needed
                post["id"] = len(posts)
                posts.append(post)
                response = {"type": "create", "post": post}

            await manager.send_message(websocket, json.dumps(response))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.disconnect(websocket)

@app.get("/")
async def get():
    """
    服務首頁的 HTML 文件。
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

