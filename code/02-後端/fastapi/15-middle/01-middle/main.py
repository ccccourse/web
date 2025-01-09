import time
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# 自定義中間件來計算請求處理時間
class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()  # 記錄請求處理的開始時間
        response = await call_next(request)  # 處理請求並獲得響應
        process_time = time.time() - start_time  # 計算請求處理的時間
        response.headers["X-Process-Time"] = str(process_time)  # 將處理時間添加到響應標頭
        print(f'X-Process-Time:{str(process_time)}')
        return response

# 創建 FastAPI 應用
app = FastAPI()

# 使用自定義中間件
app.add_middleware(TimerMiddleware)

# 範例路由
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# 另一個範例路由
@app.get("/slow")
async def read_slow():
    time.sleep(2)  # 模擬慢速操作
    return {"message": "This was a slow response!"}
