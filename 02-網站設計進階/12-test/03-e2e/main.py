from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()

# 模擬後端 API
@app.get("/api/data", response_class=JSONResponse)
async def get_data():
    return {"message": "Hello from API"}

# 提供靜態前端文件
app.mount("/", StaticFiles(directory="static", html=True), name="static")
