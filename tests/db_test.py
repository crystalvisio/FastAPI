from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config, database

from app.config import settings as st

SQLALCHEMY_URL = f"postgresql://{st.db_user}:{st.db_password}@{st.db_host}:{st.db_port}/{st.db_name}"

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override dependency
def override_get_db():
    return next(get_test_db_session())
