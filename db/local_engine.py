import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from utils.secrets import password_manager
from utils.enums import GenderEnum
from settings import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_LOCAL_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
                            bind=engine,
                            autocommit=False,
                            autoflush=False,
                            expire_on_commit=False,
                            )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()