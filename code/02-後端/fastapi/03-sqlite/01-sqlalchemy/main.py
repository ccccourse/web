from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 創建資料庫引擎
# engine = create_engine('sqlite:///:memory:', echo=True)  # 使用 SQLite 的記憶體資料庫
engine = create_engine('sqlite:///users.db', echo=True) 

# 定義基礎類別
Base = declarative_base()

# 定義 User 類別
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

# 創建資料表
Base.metadata.create_all(engine)

# 創建 session
Session = sessionmaker(bind=engine)
session = Session()

# 插入資料
user1 = User(username='alice', email='alice@example.com')
user2 = User(username='bob', email='bob@example.com')

session.add(user1)
session.add(user2)
session.commit()

# 查詢資料
users = session.query(User).all()

# 顯示查詢結果
for user in users:
    print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}')

# 關閉 session
session.close()
