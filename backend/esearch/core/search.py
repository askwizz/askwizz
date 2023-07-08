import logging
import os

from langchain.docstore.document import Document
from pydantic import BaseModel

from esearch.api.lifespan import ml_models
from esearch.services.milvus.client import Milvus
from esearch.services.milvus.entity import RetrievedPassage

token_config_path = os.path.join(os.path.dirname(__file__), "models/20B_tokenizer.json")


class SearchRequest(BaseModel):
    query: str
    generate_answer: bool = False


def get_context_from_documents(documents: list[Document]) -> str:
    sep = """
    """
    return sep.join([d.page_content for d in documents])


def generate_prompt(question: str, relevant_documents: list[Document]) -> str:
    context = get_context_from_documents(relevant_documents)
    return f"""Q & A
Given the following extracted parts of multiple documents and a question, create a final answer with references.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

DOCUMENTS:
{context}

QUESTION:
{question}
Detailed expert answer:
"""  # noqa: E501


def get_answer_and_documents(
    payload: SearchRequest,
    milvus_client: Milvus,
) -> tuple[list[RetrievedPassage], str]:
    logging.info(f"Providing answer to question {payload.query}")
    question = payload.query
    relevant_documents = milvus_client.similarity_search(question, k=10)
    return relevant_documents, ""


def search(
    payload: SearchRequest, milvus_client: Milvus
) -> tuple[list[RetrievedPassage], str]:
    ml_models["llm"]
    return get_answer_and_documents(payload, milvus_client)
