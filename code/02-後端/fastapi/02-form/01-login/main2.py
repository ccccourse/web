from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <body>
            <h2>請輸入帳號密碼</h2>
            <form action="/submit" method="post">
                <label for="username">帳號:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">密碼:</label>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="提交">
            </form>
        </body>
    </html>
    """

@app.post("/submit")
async def handle_login(password: str = Form(...), username: str = Form(...)):
    return {"message": f"帳號: {username}, 密碼: {password}"}
