import datetime
import json
import logging
import uuid
from datetime import timezone

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
    convert_from_db_row_to_entity,
    save_new_connection_in_db,
    update_connection_in_db,
)
from esearch.services.milvus.client import Milvus


def get_connection_unique_key(
    configuration: ConnectionConfiguration, source: str
) -> str:
    connection_str = json.dumps(configuration.dict())
    connection_hash = hash(f"{connection_str}{source}")
    positive_hash = (connection_hash**2) % (10**8)
    return f"CONN_{positive_hash}"


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


def create_or_update_connection(
    db: Session, connection_data: NewConnectionPayload, user_id: str
) -> Connection:
    unique_connection_key = get_connection_unique_key(
        configuration=connection_data.configuration, source=connection_data.source
    )
    existing_connection_row = (
        db.query(ConnectionRow)
        .filter(ConnectionRow.connection_key == unique_connection_key)
        .first()
    )
    connection_already_exists_with_same_configuration = (
        existing_connection_row is not None
    )
    common_data_changes = {
        "configuration": connection_data.configuration,
        "indexed_at": datetime.datetime.now(timezone.utc),
        "name": connection_data.name,
        "status": ConnectionStatus.INDEXING,
        "source": parse_source(connection_data.source),
        "user_id": user_id,
        "documents_count": 0,
        "passages_count": 0,
        "connection_key": unique_connection_key,
    }
    if connection_already_exists_with_same_configuration:
        existing_connection = convert_from_db_row_to_entity(existing_connection_row)
        new_connection = Connection(
            created_at=existing_connection.created_at,
            id_=existing_connection.id_,
            **common_data_changes,
        )
        update_connection_in_db(db, new_connection)
        return new_connection

    new_connection = Connection(
        created_at=datetime.datetime.now(timezone.utc),
        id_=str(uuid.uuid4()),
        **common_data_changes,
    )

    save_new_connection_in_db(db, new_connection)

    return new_connection


def delete_connection(
    db_session: Session, user_id: str, connection_id: str, milvus_client: Milvus
) -> None:
    logging.info(f"User {user_id} deleting connection {connection_id}")
    connection = db_session.get(ConnectionRow, connection_id)
    if connection is None:
        logging.debug("No connection found")
    if connection.user_id != user_id:  # type: ignore
        raise Exception("User does not own this connection")
    db_session.delete(connection)
    db_session.commit()
    milvus_client.delete_partition(connection.connection_key)  # type: ignore
