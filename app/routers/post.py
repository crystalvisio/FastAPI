from fastapi import Response, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


# Initialise App Router
router = APIRouter(
    tags=["Post"]
)


# Reading All...
@router.get("/post", response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Reading One...
@router.get("/get-post/{id}")
def get_post(id:int, response:Response, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        utils.id_error("Post", id)
    return {"Post_details":post}


# Creating...
@router.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostBase, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return new post

    return new_post


# Deleting...
@router.delete("/delete/{id}")
def delete_post(id:int, db: Session=Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        utils.id_error("Post", id)

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating...
@router.put("/update/{id}")
def update_post(id:int, updated_post:schemas.PostBase, db:Session=Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = models.Post(**updated_post.model_dump()).filter(models.Post.id==id)

    if post.first() == None:
        utils.id_error("Post", id)
    
    post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return {"Updated Post":post.first()}
