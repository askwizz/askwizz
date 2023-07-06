from typing import Annotated, Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from esearch.api.authorization import UserData, get_current_user
from esearch.api.exceptions import NotAuthenticatedException
from esearch.core.search import SearchRequest, search
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


def add_routes(app: FastAPI) -> None:
    @app.post("/api/search")
    async def search_route(
        search_request: SearchRequest,
        user_data: Annotated[UserData, Depends(get_current_user)],
        milvus_client: Annotated[Milvus, Depends(milvus_dependency)],
    ) -> SearchResponse:
        if user_data.user_id is None:
            raise NotAuthenticatedException()
        relevant_documents, answer = search(search_request, milvus_client=milvus_client)
        return SearchResponse(answer=answer, references=relevant_documents)
