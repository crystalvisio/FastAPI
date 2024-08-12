from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from app.config import settings

# Connect to postgreSQL server
SQLALCHEMY_URL = settings.database_url

# Create Engine
engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare Base
Base = declarative_base()

# Dependency
def get_db():

    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
