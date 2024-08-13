from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils, oauth2, database

# Initialise App Router
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # Check if the post exists in the database
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise utils.id_error("Post", vote.post_id)

    # Query to check if the user has already voted on this post
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == curr_user.id
    )
    existing_vote = vote_query.first()

    # Handling UpVote
    if vote.vote_dir == 1:  
        if existing_vote:
            if existing_vote.vote_dir == 1:
                # User has already upvoted this post
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {curr_user.id} has already upvoted post {vote.post_id}"
                )
            # If the existing vote is a downvote, update it to an upvote
            else:
                existing_vote.vote_dir = 1
                db.commit()
                return {"message": "Successfully Updated to Upvote"}

        # Create a new upvote record in the database
        new_vote = models.Vote(post_id=vote.post_id, user_id=curr_user.id, vote_dir=1)
        db.add(new_vote)
        db.commit()
        return {"message": "UpVote Successful"}

    # Handling downvote
    elif vote.vote_dir == 0:
        if existing_vote:
            if existing_vote.vote_dir == 0:
                # User has already downvoted this post
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {curr_user.id} has already downvoted post {vote.post_id}"
                )
            else:
                # If the existing vote is an upvote, update it to a downvote
                existing_vote.vote_dir = 0
                db.commit()
                return {"message": "Successfully Updated to Downote"}


        # Create a new downvote record in the database
        new_vote = models.Vote(post_id=vote.post_id, user_id=curr_user.id, vote_dir=0)
        db.add(new_vote)
        db.commit()
        return {"message": "DownVote Successful"}
    
