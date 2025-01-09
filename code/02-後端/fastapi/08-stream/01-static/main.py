from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 將 "static" 資料夾掛載為靜態檔案伺服目錄
app.mount("/static", StaticFiles(directory="../static", html=True), name="static")

