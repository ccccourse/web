from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

API_KEY = "secret_api_key"

def api_key_auth(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/secure-api-key")
def secure_endpoint(auth: None = Depends(api_key_auth)):
    return {"message": "Access granted"}
