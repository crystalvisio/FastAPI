from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from app.config import settings as st

# Connect to postgreSQL server
DATABASE_URL = f"postgresql://{st.db_user}:{st.db_password}@{st.db_host}:{st.db_port}/{st.db_name}"
SQLALCHEMY_URL = (DATABASE_URL)

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
