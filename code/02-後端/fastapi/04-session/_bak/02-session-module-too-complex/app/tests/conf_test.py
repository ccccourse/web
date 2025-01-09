# sql_app/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

# 使用 in-memory SQLite 資料庫進行測試
SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture
def test_db():
    # 創建測試用的 in-memory 資料庫
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 創建資料表
    Base.metadata.create_all(bind=engine)
    
    # 覆蓋正常的資料庫 session
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()  # 提供測試用的 session
    
    # 清理：刪除所有表格
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    # 返回測試用的 client
    return TestClient(app)
