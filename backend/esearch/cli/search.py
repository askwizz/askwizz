import logging

import click

from esearch.core.models.embeddings.e5 import E5v2
from esearch.core.models.llm.rwkv import RWKVLLMModel
from esearch.core.search import SearchRequest, get_relevant_documents
from esearch.services.milvus.client import Milvus


@click.command("search")
@click.option(
    "--query",
    type=str,
    required=True,
)
@click.option(
    "--llm_path",
    type=str,
    required=True,
)
@click.option(
    "--collection_id",
    type=str,
    required=True,
)
def search_command(
    query: str,
    llm_path: str,
    collection_id: str,
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli search \
            --query "What is a bad bank ?" \
            --llm_path "./tmp/rwkv-model.pth" \
            --collection_id "user_2Qklbs5sgdrrPJhZ8g1KtlfRmkH"
    """
    embedder = E5v2()
    milvus_client = Milvus(
        collection_id,
        embedder,
    )
    RWKVLLMModel.from_path(llm_path)
    payload = SearchRequest(
        query=query,
    )
    relevant_documents, answer = get_relevant_documents(payload, milvus_client)
    logging.info(relevant_documents)
    logging.info(answer)
