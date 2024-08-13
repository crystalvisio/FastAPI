from fastapi import Response, status, Depends, APIRouter, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, func

from app import models, schemas, utils, oauth2, database


# Initialise App Router
router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


# Reading All...
@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(
    db: Session = Depends(database.get_db), 
    curr_user:int = Depends(oauth2.get_current_user),
    limit:int = 10, 
    skip:int = 0, 
    search:Optional[str] = ""
    ):

    # Get All Posts and the total downvotes and upvotes

    #   SELECT posts.*, 
    #       COUNT(votes.post_id) FILTER (WHERE votes.vote_dir = 1) AS upvotes,
    #       COUNT(votes.post_id) FILTER (WHERE votes.vote_dir = 0) AS downvotes
    #   FROM posts 
    #   LEFT JOIN votes ON posts.id = votes.post_id 
    #   GROUP BY posts.id;

    posts = db.query(
        models.Post,
        func.count(case(((models.Vote.vote_dir == 1, 1)))).label("upvotes"),
        func.count(case(((models.Vote.vote_dir == 0, 1)))).label("downvotes")
    ).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(
        models.Post.content.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Post(s) Not Found!"
    )

    return posts


# Reading One...
@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id:int, db: Session = Depends(database.get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(
        models.Post,
        func.count(case(((models.Vote.vote_dir == 1, 1)))).label("upvotes"),
        func.count(case(((models.Vote.vote_dir == 0, 1)))).label("downvotes")
    ).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        utils.id_error("Post", id)
    
    return post


# Creating...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db:Session = Depends(database.get_db), curr_user:int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=curr_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return new post

    return new_post


# Deleting...
@router.delete("/{id}")
def delete_post(id:int, db: Session=Depends(database.get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        utils.id_error("Post", id)

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating...
@router.put("/{id}")
def edit_posts(id: int, updated_post: schemas.PostBase, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        utils.id_error("Post", id)
    
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    
    return updated_post