# crud.py

from sqlalchemy.orm import Session
from app.models import UserQuery

def get_user_queries(db: Session, user_id: int):
    return db.query(UserQuery).filter(UserQuery.user_id == user_id).all()
