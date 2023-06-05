from sqlalchemy.orm import Session

from db.models.connection import ConnectionCreate, create_connection_in_db


def create_connection(db: Session, connection_data: ConnectionCreate) -> None:
    create_connection_in_db(db, connection_data)
