import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app  # 假設 FastAPI 程式存儲在 main.py 檔案中

client = TestClient(app)

@pytest.fixture
def create_session():
    # 呼叫 /create_session API 來建立一個會話
    name = "test_user"
    response = client.post(f"/create_session/{name}")
    assert response.status_code == 200
    assert f"created session for {name}" in response.text
    # 從回應的 cookie 中提取會話 id
    session_id = response.cookies.get("cookie")
    return session_id, name

def test_create_session(create_session):
    session_id, name = create_session
    # 測試會話是否成功建立
    assert session_id is not None
    assert name == "test_user"

def test_whoami(create_session):
    session_id, _ = create_session
    # 測試取得當前使用者信息
    response = client.get("/whoami", cookies={"cookie": session_id})
    assert response.status_code == 200
    assert response.json() == {"username": "test_user"}

def test_del_session(create_session):
    session_id, _ = create_session
    # 測試刪除會話
    response = client.post("/delete_session", cookies={"cookie": session_id})
    assert response.status_code == 200
    assert response.json() == "deleted session"

    # 確認會話已經被刪除
    response = client.get("/whoami", cookies={"cookie": session_id})
    assert response.status_code == 403  # 預期因為會話已刪除而返回 403
