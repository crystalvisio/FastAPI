from sqlalchemy.orm import Session
from fastapi import status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, utils, oauth2, database


# Initialise App Router
router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If the user is not found, no need to verify password
    if not user:
        utils.invalid_credentials()

    # Verify Password
    if not utils.verify_pwd(user_credentials.password, user.password):
        utils.invalid_credentials()

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}