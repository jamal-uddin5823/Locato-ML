# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.recommender import recommend_queries
from app.database import get_db
from app.recommender import get_similar_queries
from app.models import UserQuery
from sqlalchemy import func

app = FastAPI()



@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    try:
        recommended_queries = recommend_queries(user_id, db)
        queries = db.query(UserQuery).filter(UserQuery.query_id.in_(recommended_queries)).all()
        return {"recommended_queries": [query.query_text for query in queries]}
    except HTTPException as e:
        raise e
    

@app.get("/recommendations/top/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    # Check if the user has any previous queries
    user_queries = db.query(UserQuery).filter(UserQuery.user_id == user_id).all()
    
    if not user_queries:  # If no queries made by the user
        # Fallback: Get the most popular queries from the user_queries table
        popular_queries = db.query(
            UserQuery.query_text, func.count(UserQuery.query_text).label("query_count")
        ).group_by(UserQuery.query_text).order_by(func.count(models.UserQuery.query_text).desc()).limit(5).all()

        return {"recommended_queries": [query.query_text for query in popular_queries]}
    
    # Add your collaborative filtering code here if the user has made queries
    # For example, you could find other users who made similar queries
@app.get("/recommendations/svd/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    user_queries = db.query(UserQuery).filter(UserQuery.user_id == user_id).all()
    
    if not user_queries:  # If no queries made by the user
        # Fallback: Get the most popular queries
        popular_queries = db.query(
            UserQuery.query_text, func.count(UserQuery.query_text).label("query_count")
        ).group_by(UserQuery.query_text).order_by(func.count(UserQuery.query_text).desc()).limit(5).all()

        return {"recommended_queries": [query.query_text for query in popular_queries]}
    
    # Collaborative filtering: Get similar queries to the user's queries
    similar_queries = get_similar_queries(user_queries, db)
    return {"recommended_queries": [q.query_text for q in similar_queries]}
