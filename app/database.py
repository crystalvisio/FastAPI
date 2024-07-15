import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Loading ENV variables
load_dotenv()

db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")

# Connect to postgreSQL server
SQLALCHEMY_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"

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
