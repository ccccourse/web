from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()

API_KEY = "secret_api_key"

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/secure-api-key-header")
def secure_endpoint(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return {"message": "Access granted"}
