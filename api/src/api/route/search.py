from typing import Any

from api.lifespan import ml_models
from api.route.types import SearchRequest
from core.search import search
from fastapi import FastAPI
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
    async def search_route(search_request: SearchRequest) -> SearchResponse:
        relevant_documents, answer = search(search_request, llm=ml_models["llm"])
        return SearchResponse(answer=answer, references=relevant_documents)
