from typing import Annotated, Any

from fastapi import Depends, FastAPI
from langchain.docstore.document import Document
from pydantic import BaseModel

from esearch.api.authorization import UserData, get_current_user
from esearch.api.exceptions import NotAuthenticatedException
from esearch.api.lifespan import ml_models
from esearch.core.search import SearchRequest, search


class SearchMatch(BaseModel):
    rank: int
    score: float
    reference: str
    metadata: dict[str, Any]
    index: int


class SearchResponse(BaseModel):
    answer: str
    references: list[Document]


def add_routes(app: FastAPI) -> None:
    @app.post("/api/search")
    async def search_route(
        search_request: SearchRequest,
        user_data: Annotated[UserData, Depends(get_current_user)],
    ) -> SearchResponse:
        if user_data.user_id is None:
            raise NotAuthenticatedException()
        relevant_documents, answer = search(
            search_request, llm=ml_models["llm"], user_id=user_data.user_id
        )
        return SearchResponse(answer=answer, references=relevant_documents)
