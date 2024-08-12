from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config, database

SQLALCHEMY_DATABASE_URL = config.settings.testdb_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
