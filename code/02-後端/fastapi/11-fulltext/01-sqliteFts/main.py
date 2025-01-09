import sqlite3

# 建立資料庫連線
conn = sqlite3.connect("fts_example.db")


cursor = conn.cursor()

# 建立 FTS5 表（如果尚未存在）
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS articles USING FTS5(id, title, content)")

# 插入數據
cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (1, "Python Basics", "Learn the basics of Python programming."))
cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (2, "SQLite FTS", "Full-text search with SQLite FTS is powerful and easy to use."))
cursor.execute("INSERT INTO articles (id, title, content) VALUES (?, ?, ?)", (3, "FastAPI Guide", "Build APIs quickly using FastAPI."))
conn.commit()

# 搜尋數據
query = "Python"
cursor.execute("SELECT id, title, content FROM articles WHERE articles MATCH ?", (query,))
results = cursor.fetchall()

# 顯示搜尋結果
print("Search Results:")
for result in results:
    print(f"ID: {result[0]}, Title: {result[1]}, Content: {result[2]}")

# 關閉連線
conn.close()
