# schemas.py

from pydantic import BaseModel

class UserQuerySchema(BaseModel):
    query_text: str
    user_id: int

    class Config:
        orm_mode = True
