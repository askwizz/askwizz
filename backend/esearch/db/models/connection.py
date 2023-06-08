import datetime
import uuid
from enum import StrEnum

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Session

from esearch.db.engine import Base


class ConnectionCreate(BaseModel):
    atlassian_email: str
    atlassian_token: str
    domain: str
    name: str
    user_id: str


class ConnectionStatus(StrEnum):
    Creating = "Creating"


class ConnectionRow(Base):
    __tablename__ = "connection"

    atlassian_email = Column(String(200), nullable=False)
    atlassian_token = Column(String(200), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    domain = Column(String(400), nullable=False)
    id = Column(String(20), primary_key=True)  # noqa: A003
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    user_id = Column(String(200), nullable=False)


def create_connection_in_db(
    db: Session, create_data: ConnectionCreate
) -> ConnectionRow:
    db_connection = ConnectionRow(
        atlassian_email=create_data.atlassian_email,
        atlassian_token=create_data.atlassian_token,
        created_at=datetime.datetime.now(),
        domain=create_data.domain,
        id=str(uuid.uuid4()),
        name=create_data.name,
        status=ConnectionStatus.Creating.value,
        user_id=create_data.user_id,
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection
