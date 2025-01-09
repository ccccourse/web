import os
import whisper
import websockets
import asyncio
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

# 初始化 FastAPI 應用
app = FastAPI()

# 將 "static" 資料夾掛載為靜態檔案伺服目錄
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# 載入 Whisper 模型
model = whisper.load_model("base")

# WebSocket 路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 接收錄音數據
            audio_data = await websocket.receive_bytes()

            # 儲存音訊並進行語音轉文字
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)
            
            # 轉錄音訊
            result = model.transcribe("temp_audio.wav")
            transcription = result['text']

            # 傳送回文字
            await websocket.send_text(transcription)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
