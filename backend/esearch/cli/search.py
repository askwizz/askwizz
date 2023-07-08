import logging

import click

from esearch.core.models.embeddings.e5 import E5v2
from esearch.core.models.rwkv import LLMModel
from esearch.core.search import SearchRequest, get_answer_and_documents
from esearch.services.milvus.client import Milvus


@click.command("search")
@click.option(
    "--query",
    type=str,
    required=True,
)
@click.option(
    "--generate_answer",
    type=bool,
    required=True,
    default=False,
)
@click.option(
    "--rwkv_model_path",
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
    generate_answer: bool,
    rwkv_model_path: str,
    collection_id: str,
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli search \
            --query "What is a bad bank ?" \
            --generate_answer "False" \
            --rwkv_model_path "./tmp/rwkv-model.pth" \
            --collection_id "user_2Qklbs5sgdrrPJhZ8g1KtlfRmkH"
    """
    embedder = E5v2()
    milvus_client = Milvus(
        collection_id,
        embedder,
    )
    LLMModel.from_path(rwkv_model_path)
    payload = SearchRequest(
        query=query,
        generate_answer=generate_answer,
    )
    relevant_documents, answer = get_answer_and_documents(payload, milvus_client)
    logging.info(relevant_documents)
    logging.info(answer)
