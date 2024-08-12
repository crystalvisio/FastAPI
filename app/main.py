# Import Dependencies
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models, database
from app.routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=database.engine)


# Initialize Fast API app
app = FastAPI()

# Set Up CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize app routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Root
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI.com"}
