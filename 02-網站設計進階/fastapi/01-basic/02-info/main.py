# https://fastapi.tiangolo.com/#example
from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/headers")
async def get_headers(request: Request):
    # 將請求的 headers 轉換為字典並返回
    headers_dict = {key: value for key, value in request.headers.items()}
    return JSONResponse(content=headers_dict)