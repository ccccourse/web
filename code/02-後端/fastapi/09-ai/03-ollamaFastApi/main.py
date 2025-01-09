from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import ollama

# 初始化 FastAPI
app = FastAPI()

# 定義請求結構
class QuestionInput(BaseModel):
    question: str
    history: list[str] = []  # 可選，記錄對話歷史

# 提供靜態文件
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/static/{filename}")
def serve_static(filename: str):
    return FileResponse(f"static/{filename}")

# 問答路由
@app.post("/ask")
def ask_question(input: QuestionInput):
    if not input.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        response = ollama.chat(input.question)
        return {"question": input.question, "answer": response}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
