import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}

@pytest.mark.asyncio
async def test_echo():
    payload = {"key": "value"}
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == {"echo": payload}
