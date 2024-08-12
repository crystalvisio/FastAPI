from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas, utils, database, models
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_mins

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create Acces Token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


# Verify Access Token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise utils.credentials_exception()

        token_data = schemas.TokenData(id=str(user_id))
        return token_data

    except JWTError:
        raise utils.credentials_exception()


def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(database.get_db)):

    token = verify_access_token(token)

    curr_user = db.query(models.User).filter(models.User.id == token.id).first()

    if curr_user is None:
        raise utils.id_error("Post", curr_user.id)

    return curr_user