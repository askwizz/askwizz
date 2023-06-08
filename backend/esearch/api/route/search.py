from typing import Annotated, Any

from esearch.api.authorization import TokenData, get_current_user
from esearch.api.lifespan import ml_models
from esearch.core.search import SearchRequest, search
from fastapi import Depends, FastAPI
from langchain.docstore.document import Document
from pydantic import BaseModel


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
        token_data: Annotated[TokenData, Depends(get_current_user)],
    ) -> SearchResponse:
        relevant_documents, answer = search(search_request, llm=ml_models["llm"])
        return SearchResponse(answer=answer, references=relevant_documents)
