from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2, database

# Initialise App Router
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(database.get_db), curr_user:int = Depends(oauth2.get_current_user)):

    # hashing pwd - user.password
    user.password = utils.hash_pwd(user.password) 

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # return  new user

    return new_user