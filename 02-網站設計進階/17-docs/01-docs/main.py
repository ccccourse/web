from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="這是我的 API，用於展示 FastAPI 的功能。",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"  # 更改 OpenAPI 規範的路徑
)

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
