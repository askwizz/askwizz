from typing import Annotated, Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.api.authorization import (
    UserData,
    get_current_user,
)
from esearch.api.settings import AppSettings
from esearch.core.passage.retrieve import (
    PassageTextPayload,
    get_text_from_passage_payload,
)
from esearch.core.search import SearchRequest, save_search_query, search
from esearch.db.engine import get_db
from esearch.services.milvus.client import Milvus, milvus_dependency
from esearch.services.milvus.entity import RetrievedPassage


class SearchMatch(BaseModel):
    rank: int
    score: float
    reference: str
    metadata: dict[str, Any]
    index: int


class SearchResponse(BaseModel):
    answer: str
    references: list[RetrievedPassage]


class PassageTextRequest(BaseModel):
    connection_id: str
    config: PassageTextPayload


def add_routes(app: FastAPI, settings: AppSettings) -> None:
    @app.post("/api/search")
    async def search_route(
        search_request: SearchRequest,
        user_data: Annotated[UserData, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
        milvus_client: Annotated[Milvus, Depends(milvus_dependency)],
    ) -> SearchResponse:
        save_search_query(db, user_data.user_id, search_request.query)
        relevant_documents, answer = search(
            search_request, milvus_client, db, user_data.user_id
        )
        return SearchResponse(answer=answer, references=relevant_documents)

    @app.post("/api/passage/text")
    async def passage_text(
        passage: PassageTextRequest,
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
        user_data: Annotated[UserData, Depends(get_current_user)],
    ) -> str:
        return get_text_from_passage_payload(
            db,
            user_data.user_id,
            passage.connection_id,
            passage.config,
        )
