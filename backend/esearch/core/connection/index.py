import datetime
import logging
from typing import Callable, Dict

from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Milvus
from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.core.connection.definition import (
    AtlassianData,
    Connection,
    ConnectionSource,
    ConnectionStatus,
)
from esearch.core.parsing.confluence import (
    create_passages_from_pages,
    get_confluence_pages,
)
from esearch.db.models.connection import update_connection_in_db


def get_collection_name(user_id: str) -> str:
    return user_id.replace("-", "_")


class IndexingResult(BaseModel):
    passages: int
    documents: int


def index_confluence_connection(
    connection: Connection, embedder: Embeddings
) -> IndexingResult:
    collection_name = get_collection_name(connection.user_id)
    logging.debug("Collection name", collection_name)

    atlassian_configuration: AtlassianData = connection.configuration.atlassian  # type: ignore  # noqa: E501
    pages = get_confluence_pages(
        atlassian_configuration.atlassian_domain,
        atlassian_configuration.atlassian_email,
        atlassian_configuration.atlassian_token,
    )
    passages = create_passages_from_pages(pages)
    Milvus.from_documents(
        passages,
        embedder,
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name=collection_name,
        drop_old=True,
    )
    return IndexingResult(passages=len(passages), documents=len(pages))


source_to_indexer: Dict[
    ConnectionSource, Callable[[Connection, Embeddings], IndexingResult]
] = {
    ConnectionSource.CONFLUENCE: index_confluence_connection,
}


def index_connection(connection: Connection, embedder: Embeddings, db: Session) -> None:
    result = source_to_indexer[connection.source](connection, embedder)
    connection.documents_count = result.documents
    connection.passages_count = result.passages
    connection.indexed_at = datetime.datetime.now()
    connection.status = ConnectionStatus.ACTIVE

    update_connection_in_db(db, connection)
