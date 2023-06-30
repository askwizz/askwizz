import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()


def get_database_url_from_env() -> str:
    database_url = os.environ.get("API_SQLALCHEMY_DATABASE_URL")
    assert (
        database_url is not None
    ), "API_SQLALCHEMY_DATABASE_URL environment variable is not set"
    return database_url


def get_db() -> Generator[Session, None, None]:
    # FIXME pass db url as argument
    database_url = get_database_url_from_env()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
