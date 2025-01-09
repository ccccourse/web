import sqlite3
import jieba

# 插入中文文本到資料庫
def insert_article(id, title, content):
    # 使用 jieba 進行中文分詞
    text = " ".join(jieba.cut(title+' . '+content))  # 分詞並使用空格分開
    segmented = " ".join(jieba.cut(text))

    cursor.execute("INSERT INTO articles (id, title, content, segmented) VALUES (?, ?, ?, ?)", 
                   (id, title, content, segmented))
    conn.commit()

# 建立資料庫連線
conn = sqlite3.connect("fts_example.db")


cursor = conn.cursor()

# 建立 FTS5 表（如果尚未存在）
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS articles USING FTS5(id, title, content, segmented)")

# 插入數據
insert_article(1, 'Python 基礎', '學習 Python 程式設計的基礎知識。')
insert_article(2, '快速學習 AI', '學習人工智慧的基本概念和技巧。')
insert_article(1, '棒球', '台灣贏了！')
conn.commit()

# 搜尋數據
query = "人工智慧"
cursor.execute("SELECT id, title, content, segmented FROM articles WHERE articles MATCH ?", (query,))
results = cursor.fetchall()

# 顯示搜尋結果
print("搜尋結果:")
for result in results:
    print(f"ID: {result[0]}, Title: {result[1]}, Content: {result[2]}, Segmented: {result[3]}")

# 關閉連線
conn.close()
