from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI()

# 初始化書籍資料
books = {
    "1": {
        "id": "1",
        "title": "The Hound of the Baskervilles",
        "author": "Conan Doyle, Arthur",
    },
    "2": {
        "id": "2",
        "title": "The Old Man",
        "author": "Lee Ear",
    },
}

@app.get("/")
async def read_root():
    return {"message": "Hello world!"}

@app.get("/book")
async def get_books():
    return list(books.values())

@app.get("/book/{book_id}")
async def get_book(book_id):
    if book_id in books:
        return books[book_id]
    raise HTTPException(status_code=404, detail="Book not found")
