import datetime
import logging
import time
from datetime import timezone
from typing import Callable, Dict, Generator, List, Tuple

from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.core.connection.definition import (
    AtlassianData,
    Connection,
    ConnectionSource,
    ConnectionStatus,
)
from esearch.core.models.embeddings.e5 import CustomEmbeddings
from esearch.core.parsing.confluence import (
    get_confluence_passages_generator,
)
from esearch.core.passage.definition import Passage
from esearch.db.models.connection import update_connection_in_db
from esearch.services.milvus.client import Milvus


def get_collection_name(user_id: str) -> str:
    return user_id.replace("-", "_")


class IndexingResult(BaseModel):
    passages: int
    documents: int


def get_confluence_passages(
    connection: Connection,
) -> Generator[Tuple[List[Passage], int], None, None]:
    collection_name = get_collection_name(connection.user_id)
    logging.info(f"Collection name {collection_name}")

    atlassian_configuration: AtlassianData = connection.configuration.atlassian  # type: ignore  # noqa: E501
    return get_confluence_passages_generator(
        connection.id_,
        atlassian_configuration.atlassian_domain,
        atlassian_configuration.atlassian_email,
        atlassian_configuration.atlassian_token,
    )


def index_passages(
    passages_generator: Generator[Tuple[List[Passage], int], None, None],
    connection: Connection,
    embedder: CustomEmbeddings,
    milvus_client: Milvus,
) -> IndexingResult:
    passage_count = 0
    page_count = 0
    batch_id = 0
    for passages, page_count in passages_generator:  # noqa: B007
        logging.info(f"Indexing {len(passages)} passages")
        is_first_batch = batch_id == 0
        milvus_client.index_passages(
            embedder=embedder,
            passages=passages,
            connection_key=connection.connection_key,
            is_first_batch=is_first_batch,
        )
        passage_count += len(passages)
        batch_id += 1
    return IndexingResult(passages=passage_count, documents=page_count)


source_to_passages_generator: Dict[
    ConnectionSource,
    Callable[[Connection], Generator[Tuple[List[Passage], int], None, None]],
] = {
    ConnectionSource.CONFLUENCE: get_confluence_passages,
}


def index_connection(
    connection: Connection,
    embedder: CustomEmbeddings,
    db: Session,
    milvus_client: Milvus,
) -> None:
    logging.info(f"Starting indexing connection {connection.id_}")
    t1 = time.time()
    passage_generator = source_to_passages_generator[connection.source](connection)
    indexing_result = index_passages(
        passage_generator, connection, embedder, milvus_client
    )
    logging.info(
        f"Finished indexing connection {connection.id_} in {time.time() - t1:.2f}s"
    )
    connection.documents_count = indexing_result.documents
    connection.passages_count = indexing_result.passages
    connection.indexed_at = datetime.datetime.now(timezone.utc)
    connection.status = ConnectionStatus.ACTIVE

    update_connection_in_db(db, connection)
