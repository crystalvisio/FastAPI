from fastapi import status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


# Initialise App Router
router = APIRouter(
    tags=["Authentication"]
)


# @router.post("/login")
# def login(user_credentials: schemas.UserLogin, db: Session=Depends(get_db)):
    
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
#     # If the user is not found, no need to verify password
#     if not user:
#         utils.invalid_credentials()

#     # Verify Password
#     if not utils.verify_pwd(user_credentials.password, user.password):
#         utils.invalid_credentials()

#     access_token = oauth2.create_access_token(data={"user_id":user.id})
    
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If the user is not found, no need to verify password
    if not user:
        utils.invalid_credentials()

    # Verify Password
    if not utils.verify_pwd(user_credentials.password, user.password):
        utils.invalid_credentials()

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}