import datetime
import uuid

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Session

from db.engine import Base


class ConnectionCreate(BaseModel):
    name: str
    user_id: str
    atlassian_token: str
    atlassian_email: str


class Connection(Base):
    __tablename__ = "connection"

    id = Column(String(20), primary_key=True)  # noqa: A003
    name = Column(String(100), nullable=False)
    user_id = Column(String(200), nullable=False)
    atlassian_token = Column(String(200), nullable=False)
    atlassian_email = Column(String(200), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    status = Column(String(50), nullable=False)


def create_connection_in_db(db: Session, create_data: ConnectionCreate) -> Connection:
    db_connection = Connection(
        id=str(uuid.uuid4()),
        name=create_data.name,
        user_id=create_data.user_id,
        atlassian_token=create_data.atlassian_token,
        atlassian_email=create_data.atlassian_email,
        created_at=datetime.datetime.now(),
        status="Creating",
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection
