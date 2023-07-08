import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ConnectionStatus(Enum):
    INDEXING = "INDEXING"
    ACTIVE = "ACTIVE"


class ConnectionSource(Enum):
    CONFLUENCE = "CONFLUENCE"


class AtlassianData(BaseModel):
    atlassian_email: str
    atlassian_token: str
    atlassian_domain: str


class ConnectionConfiguration(BaseModel):
    atlassian: Optional[AtlassianData] = None


class Connection(BaseModel):
    id_: str
    configuration: ConnectionConfiguration
    created_at: datetime.datetime
    indexed_at: datetime.datetime
    name: str
    status: ConnectionStatus
    source: ConnectionSource
    user_id: str
    documents_count: int = 0
    passages_count: int = 0
    connection_key: str = ""
