from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.models.connection import (
    ConnectionCreate,
    ConnectionRow,
    create_connection_in_db,
)


class ConnectionEntity(BaseModel):
    atlassian_email: str
    atlassian_token: str
    created_at: str
    domain: str
    id: str
    name: str
    status: str
    user_id: str


def convert_from_db_row_to_entity(row: ConnectionRow) -> ConnectionEntity:
    return ConnectionEntity(
        atlassian_email=row.atlassian_email,
        atlassian_token=row.atlassian_token,
        created_at=str(row.created_at),
        domain=row.domain,
        id=row.id,
        name=row.name,
        status=row.status,
        user_id=row.user_id,
    )


def create_connection(
    db: Session, connection_data: ConnectionCreate
) -> ConnectionEntity:
    return convert_from_db_row_to_entity(create_connection_in_db(db, connection_data))
