from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
SQLALCHEMY_DATABASE_URL = f"sqlite:////{BASE_PATH}/storage/i75data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
