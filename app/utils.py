from fastapi import HTTPException, status
from passlib.context import CryptContext

# Define hashing algorithm
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# create hash
def hash_pwd (password:str) -> str:
    return pwd_context.hash(password)


# Verify hash
def verify_pwd(password:str):
    pass 


# Error Message:
def id_error(resoure:str, id:int):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{resoure} with id: {id} was not found"
    )
