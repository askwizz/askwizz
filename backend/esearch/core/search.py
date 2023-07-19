import datetime
import logging
import os
import uuid
from typing import List

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from esearch.api.lifespan import ML_MODELS
from esearch.core.passage.retrieve import get_text_from_passage
from esearch.core.search_history.definition import SearchHistory
from esearch.db.constants import MAX_QUERY_SIZE
from esearch.db.models.search_history import (
    get_search_history_from_user,
    save_search_into_db,
)
from esearch.services.milvus.client import Milvus
from esearch.services.milvus.entity import RetrievedPassage

token_config_path = os.path.join(os.path.dirname(__file__), "models/20B_tokenizer.json")


class SearchRequest(BaseModel):
    query: str = Field(max_length=MAX_QUERY_SIZE)
    query_texts: bool = False


def get_relevant_documents(
    payload: SearchRequest,
    milvus_client: Milvus,
) -> List[RetrievedPassage]:
    logging.info(f"Providing answer to question {payload.query}")
    question = payload.query
    return milvus_client.similarity_search(question, k=10)


def add_text_to_passage(db: Session, user_id: str, passage: RetrievedPassage) -> None:
    try:
        text = get_text_from_passage(db, user_id, passage.metadata)
        passage.text = text
    except:  # noqa: E722
        logging.exception("Could not retrieve text from passage")
        passage.text = ""


def add_texts_to_passages(
    db: Session, user_id: str, passages: list[RetrievedPassage]
) -> None:
    for passage in passages:
        add_text_to_passage(db, user_id, passage)


def search(
    payload: SearchRequest,
    milvus_client: Milvus,
    db: Session,
    user_id: str,
) -> List[RetrievedPassage]:
    ML_MODELS["llm"]
    documents = get_relevant_documents(payload, milvus_client)
    if payload.query_texts:
        add_texts_to_passages(db, user_id, documents)
    return documents


def save_search_query(db: Session, user_id: str, query: str) -> None:
    search = SearchHistory(
        id_=str(uuid.uuid4()),
        user_id=user_id,
        search=query,
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )
    save_search_into_db(db, search)


def get_search_history(db: Session, user_id: str) -> List[SearchHistory]:
    return get_search_history_from_user(db, user_id)
