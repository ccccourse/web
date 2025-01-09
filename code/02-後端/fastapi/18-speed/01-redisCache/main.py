import redis
from fastapi import FastAPI, HTTPException
from typing import Optional

# 初始化 FastAPI 應用
app = FastAPI()

# 初始化 Redis 客戶端
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# 模擬的資料庫查詢函數
def fetch_item_from_db(item_id: int) -> Optional[str]:
    # 假設我們的資料庫中有一個字典來存儲物品
    db = {
        1: "Item 1",
        2: "Item 2",
        3: "Item 3",
    }
    return db.get(item_id)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # 嘗試從 Redis 中獲取緩存的資料
    cached_item = redis_client.get(f"item:{item_id}")
    print(f'cached_item={cached_item}')
    # 如果存在緩存，則返回緩存的結果
    if cached_item:
        return {"item": cached_item}

    # 如果沒有緩存，從資料庫查詢
    item = fetch_item_from_db(item_id)
    print(f'fetch_item_from_db={item}')
    
    # 如果資料庫中沒有該項目，返回 404 錯誤
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # 將資料存入 Redis 緩存，並設置過期時間為 60 秒
    redis_client.setex(f"item:{item_id}", 60, item)

    return {"item": item}
