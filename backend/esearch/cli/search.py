import logging

import click
from langchain.vectorstores import Milvus

from esearch.core.index_confluence import get_collection_name_from_connection
from esearch.core.models.embeddings.e5 import E5Basev2
from esearch.core.models.rwkv import LLMModel
from esearch.core.search import SearchRequest, get_answer_and_documents


@click.command("search")
@click.option(
    "--query",
    type=str,
    required=True,
)
@click.option(
    "--connection_name",
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
def search_command(
    query: str, connection_name: str, generate_answer: bool, rwkv_model_path: str
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli search \
            --query "What is a bad bank ?" \
            --connection_name "From_CLI" \
            --generate_answer "False" \
            --rwkv_model_path "./tmp/rwkv-model.pth"
    """
    embedder = E5Basev2()
    vector_db = Milvus(
        embedding_function=embedder,
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name=get_collection_name_from_connection(connection_name),
    )
    llm = LLMModel.from_path(rwkv_model_path)
    payload = SearchRequest(
        query=query,
        connection_name=connection_name,
        generate_answer=generate_answer,
    )
    relevant_documents, answer = get_answer_and_documents(payload, vector_db, llm)
    logging.info(relevant_documents)
    logging.info(answer)
