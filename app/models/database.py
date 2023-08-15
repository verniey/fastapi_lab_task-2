from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/app_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
