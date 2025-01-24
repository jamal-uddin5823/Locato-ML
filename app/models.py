# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    rating = Column(Float, default=0)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    user_queries = relationship("UserQuery", back_populates="user")


class UserQuery(Base):
    __tablename__ = "user_queries"

    query_id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="user_queries")
