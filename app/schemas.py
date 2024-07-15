from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published:bool 
    # created_at: datetime


class PostResponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name:str 
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    created_at:datetime


    class Config:
        from_attributes = True


class UserGet(BaseModel):
    id:int
    name:str
    created_at:datetime


    class Config:
        from_attributes = True