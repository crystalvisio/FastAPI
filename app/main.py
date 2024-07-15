# Import Important Libraries
import psycopg2
from typing import Optional
from fastapi.params import Body
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends

from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


# Initialize Fast API app
app = FastAPI()

# Error Message:
def raise_error(id:int):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found"
    )


# Root 
@app.get("/")
def home():
    return {"message": "Welcome to my API!!!"}


# Reading All...
@app.get("/post")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Reading One...
@app.get("/get-post/{id}")
def get_post(id:int, response:Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise_error(id)
    return {"Post_details":post}


# Creating...
@app.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostBase, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return new post

    return new_post


# Deleting...
@app.delete("/delete/{id}")
def delete_post(id:int, db: Session=Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise_error(id)

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating...
@app.put("/update/{id}")
def update_post(id:int, updated_post:schemas.PostBase, db:Session=Depends(get_db)):

    post = models.Post(**updated_post.model_dump()).filter(models.Post.id==id)

    if post.first() == None:
        raise_error(id)
    
    post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return {"Updated Post":post.first()}


# Creating User
@app.post("/create-user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing pwd - user.password
    user.password = utils.hash_pwd(user.password) 

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # return  new user

    return new_user