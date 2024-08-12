from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional 


# Create New User Response Model Schema
class UserBase(BaseModel):
    id:int
    name:str
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True


# Default Post Schema without `id` and `user` for creation
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config:
        from_attributes = True


# Schema for response which includes `id` and `user`
class PostResponse(PostBase):
    id: int
    user: UserBase

    class Config:
        from_attributes = True


# Schema for response which includes upvotes and downvotes
class PostOut(BaseModel):
    Post: PostResponse
    upvotes: int
    downvotes: int

    class Config:
        from_attributes = True


# Schema for creating a post
class PostCreate(PostBase):
    pass


# Create New User Schema
class UserCreate(BaseModel):
    name:str 
    email:EmailStr
    password:str


# Get Users Schema
class UserGet(BaseModel):
    id:int
    name:str
    created_at:datetime

    class Config:
        from_attributes = True


# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Response Schema
class Token(BaseModel):
    access_token: str
    token_type: str


# Token Data Schema (Add more info if you wanna add more to the signature header)
class TokenData(BaseModel):
    id: Optional[str] = None


# Votes Schema
class Vote(BaseModel):
    post_id:int
    vote_dir:conint(ge=0, le=1)  # type: ignore # Ensures vote_vote_dir is 0 or 1