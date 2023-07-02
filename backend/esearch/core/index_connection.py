import logging

from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Milvus

from esearch.core.connection import ConnectionEntity
from esearch.core.index_confluence import (
    get_collection_name_from_connection,
    get_confluence_pages_from_domain,
)
from esearch.core.parsing.confluence import create_documents_from_pages
from esearch.db.models.connection import ConnectionStatus


def index_confluence_connection(
    connection: ConnectionEntity, embedder: Embeddings
) -> None:
    collection_name = get_collection_name_from_connection(connection.name)
    logging.debug("Collection name", collection_name)

    pages = get_confluence_pages_from_domain(
        connection.domain,
        connection.atlassian_email,
        connection.atlassian_token,
    )
    documents = create_documents_from_pages(pages)
    Milvus.from_documents(
        documents,
        embedder,
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name=collection_name,
        drop_old=True,
    )


def index_connection(connection: ConnectionEntity, embedder: Embeddings) -> None:
    if connection.status != ConnectionStatus.Creating.value:  # type: ignore
        return
    index_confluence_connection(connection, embedder)
