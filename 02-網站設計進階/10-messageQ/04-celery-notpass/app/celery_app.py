from celery import Celery

# 初始化 Celery
celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0",  # 使用 Redis 作為 Broker
    backend="redis://localhost:6379/0" # 使用 Redis 作為結果存儲
)

celery_app.conf.task_routes = {
    "tasks.example_task": {"queue": "default"}
}
