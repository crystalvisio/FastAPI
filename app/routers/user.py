from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


# Initialise App Router
router = APIRouter(
    prefix="/user",
    tags=["User"]
)


# Creating User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_users(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing pwd - user.password
    user.password = utils.hash_pwd(user.password) 

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # return  new user

    return new_user


# Getting User by id
@router.get("/{id}", response_model=schemas.UserGet)
def get_users(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id).first()

    print(user.id)

    if not user:
        utils.id_error("User", id)

    return user