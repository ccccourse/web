from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 資料庫設定
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料庫初始化
def init_db():
    from app import models  # 確保導入模型以創建資料表
    Base.metadata.create_all(bind=engine)

# 資料庫會話依賴項
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
