from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional 


class PostBase(BaseModel):
    title:str
    content:str
    published:bool 
    # created_at: datetime


class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    user_id:int
    user:UserOut

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name:str 
    email:EmailStr
    password:str


class UserGet(BaseModel):
    id:int
    name:str
    created_at:datetime


    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[str] = None