from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")
expire_mins = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# Create Acces Token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.now() + timedelta(minutes=int(expire_mins))
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode, secret_key, algo)

    return encoded_jwt