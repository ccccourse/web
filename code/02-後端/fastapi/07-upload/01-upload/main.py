import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

# 創建 FastAPI 應用
app = FastAPI()

# 設定檔案儲存資料夾
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 若資料夾不存在則自動建立

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    提供檔案上傳的前端 HTML 表單
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>檔案上傳範例</title>
    </head>
    <body>
        <h1>檔案上傳範例</h1>
        <form action="/upload/single/" method="post" enctype="multipart/form-data">
            <label for="file">選擇檔案：</label>
            <input type="file" id="file" name="file" required>
            <button type="submit">上傳</button>
        </form>
        <hr>
        <h2>多檔案上傳</h2>
        <form action="/upload/multiple/" method="post" enctype="multipart/form-data">
            <label for="files">選擇檔案（可多選）：</label>
            <input type="file" id="files" name="files" multiple required>
            <button type="submit">上傳</button>
        </form>
        <hr>
        <h2>檔案與表單資料上傳</h2>
        <form action="/upload/with-form/" method="post" enctype="multipart/form-data">
            <label for="description">描述：</label>
            <input type="text" id="description" name="description" required>
            <br><br>
            <label for="file">選擇檔案：</label>
            <input type="file" id="file" name="file" required>
            <button type="submit">上傳</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload/single/")
async def upload_single_file(file: UploadFile):
    """
    處理單檔案上傳，並將檔案儲存到伺服器
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {
        "message": "檔案已儲存",
        "filename": file.filename,
        "file_path": file_path,
    }

@app.post("/upload/multiple/")
async def upload_multiple_files(files: list[UploadFile]):
    """
    處理多檔案上傳，並將檔案儲存到伺服器
    """
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_files.append({
            "filename": file.filename,
            "file_path": file_path,
        })
    return {
        "message": "所有檔案已儲存",
        "files": saved_files,
    }

@app.post("/upload/with-form/")
async def upload_file_with_form_data(
    description: str = Form(...),
    file: UploadFile = File(...),
):
    """
    處理檔案與表單資料上傳，並將檔案儲存到伺服器
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {
        "message": "檔案與表單資料已儲存",
        "description": description,
        "filename": file.filename,
        "file_path": file_path,
    }
