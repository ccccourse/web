from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World"}

@app.post("/echo")
async def echo(data: dict):
    return {"echo": data}
