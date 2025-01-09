from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

@app.get("/video/")
async def stream_video(request: Request):
    file_path = "../static/test.mp4"
    
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # 打開檔案
    file = open(file_path, mode="rb")
    
    # 取得 Range 標頭，並解析起始與結束位置
    range_header = request.headers.get('Range')
    if range_header:
        # 解析 Range 標頭，例如 "bytes=0-1023"
        byte_range = range_header.split('=')[1].split('-')
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else None
        
        # 設定檔案的讀取位置
        file.seek(start)
        
        # 根據 end 是否為 None 決定讀取範圍
        content = file.read(end - start if end else None)
        
        # 如果 end 是 None，則不要做 end - 1 的運算
        if end is None:
            content_range = f"bytes {start}-{os.path.getsize(file_path)-1}/{os.path.getsize(file_path)}"
        else:
            content_range = f"bytes {start}-{end-1}/{os.path.getsize(file_path)}"
        
        # 回傳部份檔案內容
        return StreamingResponse(iter([content]), media_type="video/mp4", headers={"Content-Range": content_range})
    
    # 如果沒有 Range 標頭，傳送整個檔案
    return StreamingResponse(file, media_type="video/mp4")
