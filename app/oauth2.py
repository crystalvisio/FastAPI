import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from . import schemas, utils


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create Acces Token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)

    return encoded_jwt


# Verify Access Token
def verify_access_token(token:str):

    try:
        payload = jwt.decode(token, secret_key, algorithms=ALGORITHM)
        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))
    
    except JWTError:
        raise utils.credentials_exception
    
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme)):
    
    return verify_access_token(token)