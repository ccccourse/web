from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from .tasks import example_task

app = FastAPI()

@app.post("/process")
async def process_data(data: str):
    task = example_task.apply_async(args=[data])  # 提交 Celery 任務
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)  # 獲取任務狀態
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.successful() else None
    }
