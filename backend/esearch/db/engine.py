import os
from typing import Callable, Generator

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session


class Base(DeclarativeBase):
    type_annotation_map = {
        str: String().with_variant(String(255), "mysql", "mariadb"),
    }


def get_database_url_from_env() -> str:
    database_url = os.environ.get("API_SQLALCHEMY_DATABASE_URL")
    assert (
        database_url is not None
    ), "API_SQLALCHEMY_DATABASE_URL environment variable is not set"
    return database_url


def get_db(database_url: str) -> Callable[[], Generator[Session, None, None]]:
    def get_db_generator() -> Generator[Session, None, None]:
        engine = create_engine(database_url)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        db = session_local()
        try:
            yield db
        finally:
            db.close()

    return get_db_generator
