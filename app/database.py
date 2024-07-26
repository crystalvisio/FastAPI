from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

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
