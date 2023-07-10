import json
from typing import List

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from esearch.core.connection.definition import Connection, ConnectionConfiguration
from esearch.db.engine import Base


class ConnectionRow(Base):
    __tablename__ = "connection"

    id = Column(String(20), primary_key=True)  # noqa: A003
    configuration = Column(JSON, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    indexed_at = Column(DateTime(), nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)
    user_id = Column(String(200), nullable=False)
    documents_count = Column(Integer, nullable=False)
    passages_count = Column(Integer, nullable=False)
    connection_key = Column(String(256), nullable=False)


def convert_from_db_row_to_entity(row: ConnectionRow) -> Connection:
    return Connection(
        configuration=ConnectionConfiguration(**json.loads(row.configuration)),  # type: ignore  # noqa: E501
        created_at=row.created_at,  # type: ignore
        indexed_at=row.indexed_at,  # type: ignore
        id_=row.id,  # type: ignore
        name=row.name,  # type: ignore
        status=row.status,  # type: ignore
        source=row.source,  # type: ignore
        user_id=row.user_id,  # type: ignore
        documents_count=row.documents_count,  # type: ignore
        passages_count=row.passages_count,  # type: ignore
        connection_key=row.connection_key,  # type: ignore
    )


def get_serializable_connection(connection: Connection) -> dict:
    return {
        "configuration": connection.configuration.json(),
        "created_at": connection.created_at,
        "indexed_at": connection.indexed_at,
        "id": connection.id_,
        "name": connection.name,
        "status": connection.status.value,
        "source": connection.source.value,
        "user_id": connection.user_id,
        "documents_count": connection.documents_count,
        "passages_count": connection.passages_count,
        "connection_key": connection.connection_key,
    }


def convert_from_entity_to_db_row(connection: Connection) -> ConnectionRow:
    return ConnectionRow(**get_serializable_connection(connection))


def save_new_connection_in_db(db: Session, connection: Connection) -> None:
    db.add(convert_from_entity_to_db_row(connection))
    db.commit()


def update_connection_in_db(db: Session, connection: Connection) -> None:
    db.query(ConnectionRow).filter(ConnectionRow.id == connection.id_).update(
        get_serializable_connection(connection)
    )
    db.commit()


def fetch_connections_of_user(db: Session, user_id: str) -> List[Connection]:
    return [
        convert_from_db_row_to_entity(row)
        for row in db.query(ConnectionRow).filter(ConnectionRow.user_id == user_id)
    ]


def fetch_connection_of_user(
    db: Session, user_id: str, connection_id: str
) -> Connection:
    connection = convert_from_db_row_to_entity(
        db.query(ConnectionRow).filter(ConnectionRow.id == connection_id).one()
    )
    if connection.user_id != user_id:
        raise Exception("Connection not found")
    return connection
