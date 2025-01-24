# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.recommender import recommend_queries
from app.database import get_db
from app.routes import recommend

app = FastAPI()
app.include_router(recommend.router)


@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    try:
        recommended_queries = recommend_queries(user_id, db)
        queries = db.query(UserQuery).filter(UserQuery.query_id.in_(recommended_queries)).all()
        return {"recommended_queries": [query.query_text for query in queries]}
    except HTTPException as e:
        raise e
