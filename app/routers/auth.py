from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


# Initialise App Router
router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials:schemas.UserLogin, db: Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # If the user is not found, no need to verify password
    if not user:
        utils.invalid_credentials()

    # Verify Password
    if not utils.verify_pwd(user_credentials.password, user.password):
        utils.invalid_credentials()
    
    return {"Message": "Login Succesful"}