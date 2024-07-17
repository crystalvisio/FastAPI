import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, utils, database, models

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create Acces Token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)

    return encoded_jwt


# Verify Access Token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise utils.credentials_exception

        token_data = schemas.TokenData(id=str(user_id))
        return token_data

    except JWTError as e:
        raise utils.credentials_exception from e


def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(database.get_db)):

    token = verify_access_token(token)

    curr_user = db.query(models.User).filter(models.User.id == token.id).first()

    if curr_user is None:
        raise utils.id_error("Post", curr_user.id)
    
    return curr_user