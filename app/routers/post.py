from fastapi import Response, status, Depends, APIRouter, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


# Initialise App Router
router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


# Reading All...
@router.get("/", response_model=List[schemas.PostResponse])
def read_all(
    db: Session = Depends(get_db), 
    curr_user:int = Depends(oauth2.get_current_user),
    limit:int = 10, 
    skip:int = 0, 
    search:Optional[str] = ""
    ):

    posts = db.query(models.Post).filter(models.Post.content.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Post(s) Not Found!"
    )

    return posts


# Reading One...
@router.get("/{id}", response_model=schemas.PostResponse)
def read_one(id:int, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        utils.id_error("Post", id)
    
    return post


# Creating...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostBase, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    print(curr_user.id)

    new_post = models.Post(user_id=curr_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return new post

    return new_post


# Deleting...
@router.delete("/{id}")
def delete_post(id:int, db: Session=Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        utils.id_error("Post", id)

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating...
@router.put("/{id}")
def update_posts(id:int, updated_post:schemas.PostBase, db:Session=Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = models.Post(**updated_post.model_dump()).filter(models.Post.id==id)

    if post.first() == None:
        utils.id_error("Post", id)
    
    post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post.first()
