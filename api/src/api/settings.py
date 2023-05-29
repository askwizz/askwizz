from pathlib import Path

import faiss
from pydantic import BaseModel, BaseSettings, Field

from indexer.database import Database


class OAuthConfig(BaseModel):
    client_id: str
    client_secret: str


class AppSettings(BaseSettings):
    oauth_atlassian: OAuthConfig = Field(default=...)
    index: Path | faiss.IndexIDMap = Field(default=...)
    database: Path | Database = Field(default=...)

    class Config:
        env_prefix = "api_"
        env_nested_delimiter = "__"
