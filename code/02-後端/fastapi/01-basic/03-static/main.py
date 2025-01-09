from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# 將 "static" 資料夾掛載為靜態檔案伺服目錄
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# 根路徑重定向到 static/index.html
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

