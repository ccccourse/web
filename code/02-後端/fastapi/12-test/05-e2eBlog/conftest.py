import pytest
import subprocess
import time

@pytest.fixture(scope="module", autouse=True)
def test_server():
    # 啟動 FastAPI 測試伺服器
    process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(2)  # 等待伺服器啟動
    yield
    process.terminate()  # 測試結束後關閉伺服器
