from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published:bool 
    # created_at: datetime


class Response(BaseModel):
    title:str
    content:str
    published:bool 

    class Config:
        from_attributes = True