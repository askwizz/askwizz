import datetime
import uuid

from pydantic import BaseModel, root_validator, validator
from sqlalchemy.orm import Session

from esearch.core.connection.definition import (
    Connection,
    ConnectionConfiguration,
    ConnectionSource,
    ConnectionStatus,
)
from esearch.db.models.connection import (
    ConnectionRow,
    save_new_connection_in_db,
)


class NewConnectionPayload(BaseModel):
    name: str
    configuration: ConnectionConfiguration
    source: str

    @validator("source")
    def source_must_be_valid(
        cls: "NewConnectionPayload", source: str  # noqa: N805
    ) -> str:
        if source not in ConnectionSource.__members__:
            raise ValueError(f"Invalid source: {source} is not handled")  # noqa: TRY003
        return source

    @root_validator()
    def check_card_number_omitted(
        cls: "NewConnectionPayload", values: dict  # noqa: N805
    ) -> dict:
        if "configuration" not in values:
            raise ValueError("configuration must be specified")
        if "source" not in values:
            raise ValueError("source must be specified")
        if (
            values["source"] == ConnectionSource.CONFLUENCE
            and values["configuration"]["atlassian"] is None
        ):
            raise ValueError("atlassian must be specified for confluence connection")

        return values


def parse_source(source: str) -> ConnectionSource:
    if source not in ConnectionSource.__members__:
        raise ValueError(f"Invalid source: {source} is not handled")  # noqa: TRY003
    return ConnectionSource(source)


def create_connection(
    db: Session, connection_data: NewConnectionPayload, user_id: str
) -> Connection:
    new_connection = Connection(
        configuration=connection_data.configuration,
        created_at=datetime.datetime.now(),
        indexed_at=datetime.datetime.now(),
        id_=str(uuid.uuid4()),
        name=connection_data.name,
        status=ConnectionStatus.INDEXING,
        source=parse_source(connection_data.source),
        user_id=user_id,
        documents_count=0,
        passages_count=0,
    )

    save_new_connection_in_db(db, new_connection)

    return new_connection


def delete_connection(db_session: Session, user_id: str, connection_id: str) -> None:
    connection = db_session.get(ConnectionRow, connection_id)
    if connection.user_id != user_id:  # type: ignore
        raise Exception("User does not own this connection")
    db_session.delete(connection)
    db_session.commit()
