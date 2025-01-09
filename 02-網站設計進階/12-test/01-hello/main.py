from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}
