from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 初始化 FastAPI 應用程式
app = FastAPI()

# 配置靜態文件服務
app.mount("/static", StaticFiles(directory="./static", html=True), name="static")

# 配置資料庫
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 啟用 CORS（允許跨來源請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可設定為前端的 URL，例如 "http://127.0.0.1:8000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義 SQL 請求模型
class SQLQuery(BaseModel):
    query: str

# 資料庫會話依賴
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/api/execute_sql/")
async def execute_sql(sql_query: SQLQuery, db: Session = Depends(get_db)):
    print(f"sql_query={sql_query}")
    try:
        # 執行 SQL 查詢
        query = text(sql_query.query)
        print(f"text(sql_query.query)={query}")
        result = db.execute(query)

        print(f'result={result}')
        print(f'result.returns_rows={result.returns_rows}')
        # 如果是 SELECT，嘗試返回行數
        if result.returns_rows:
            rows = result.fetchall()
            print(f'rows={rows}')
            columns = result.keys()
            rows_dict = [dict(zip(columns, row)) for row in rows]
            print(f'rows_dict={rows_dict}')
            # result_dict = [dict(row) for row in rows]
            # print(f"result_dict={result_dict}")
            return {"success": True, "result": rows_dict}
        else:
            # 其他語句（如 CREATE、INSERT 等），返回成功訊息
            db.commit()  # 提交資料庫變更
            return {"success": True, "message": "Query executed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

