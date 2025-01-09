from sqlalchemy import Column, Integer, String
from app.database import Base

# 資料庫模型
class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
