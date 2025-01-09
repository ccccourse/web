import sqlite3

# 建立資料庫連線，這裡會使用一個名為 example.db 的檔案
# 如果你不需要持久化儲存，可以使用 ':memory:' 建立內存中的資料庫
connection = sqlite3.connect('example.db')  

try:
    cursor = connection.cursor()
    
    # 建立 users 資料表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE
    );
    ''')
    print("資料表建立完成")
    
    # 插入數據
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');")
        cursor.execute("INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com');")
        connection.commit()
        print("數據插入完成")
    except sqlite3.IntegrityError as e:
        print(f"插入失敗: {e}")
    
    # 查詢數據
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    print("查詢結果:")
    for row in rows:
        print(row)
    
finally:
    # 關閉連線
    connection.close()
    print("資料庫連線已關閉")
