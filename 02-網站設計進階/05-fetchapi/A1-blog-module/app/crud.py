from sqlalchemy.orm import Session
from app.models import Article

# 創建貼文
def create_article(db: Session, title: str, content: str):
    new_article = Article(title=title, content=content)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# 獲取所有貼文
def get_all_articles(db: Session):
    return db.query(Article).all()

# 獲取單一貼文
def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()
