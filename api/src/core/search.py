import os

from api.lifespan import ml_models
from core.index_confluence import get_collection_name_from_space_key
from core.models.rwkv import LLMModel
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.vectorstores import Milvus
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel

load_dotenv()

token_config_path = os.path.join(os.path.dirname(__file__), "models/20B_tokenizer.json")


class SearchRequest(BaseModel):
    query: str
    confluence_space_key: str


def log_generation_live(s: str) -> None:
    print(s, end="", flush=True)


def get_context_from_documents(documents: list[Document]) -> str:
    sep = """
    """
    return sep.join([d.page_content for d in documents])


def generate_prompt(
    question: str, relevant_documents: list[Document]
) -> tuple[list[Document], str]:
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
    payload: SearchRequest, vector_db: VectorStore, llm: LLMModel
) -> tuple[list[Document], str]:
    question = payload.query
    relevant_documents = vector_db.similarity_search(question, k=10)
    prompt = generate_prompt(question, relevant_documents)
    answer = llm.answer_prompt(prompt, log_generation_live)
    return relevant_documents, answer


def search(payload: SearchRequest, llm: LLMModel) -> tuple[list[Document], str]:
    vector_db = Milvus(
        embedding_function=ml_models["embedder"],
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name=get_collection_name_from_space_key(
            payload.confluence_space_key
        ),
    )

    return get_answer_and_documents(payload, vector_db, llm)