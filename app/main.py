# Import Important Libraries
import psycopg2
from typing import Optional, List
from fastapi.params import Body
from sqlalchemy.orm import Session
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


# Initialize Fast API app
app = FastAPI()


# Initialize app routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Root 
@app.get("/")
def home():
    return {"message": "Welcome to my API!!!"}
