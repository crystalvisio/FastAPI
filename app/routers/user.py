from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils, database, decorator, oauth2


# Initialise App Router
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Creating User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_users(user:schemas.UserCreate, db: Session = Depends(database.get_db)):

    # hashing pwd - user.password
    user.password = utils.hash_pwd(user.password)

    # Assign a default user role during account creation
    default_role = db.query(models.Role).filter(models.Role.name == "user").first()

    new_user = models.User(**user.model_dump(), role_id = default_role.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # return  new user

    return new_user


# Getting User by id
@router.get("/{id}", response_model=schemas.UserGet)
@decorator.admin_or_mod
def get_users(id:int, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        utils.id_error("User", id)

    return user