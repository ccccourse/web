from .celery_app import celery_app
import time

@celery_app.task
def example_task(data: str) -> str:
    time.sleep(5)  # 模擬耗時操作
    return f"Processed {data}"
