from typing import Any
from faiss import IndexFlatIP

from fastapi import FastAPI
from indexer.encoder import load_retriever
from pydantic import BaseModel

from api.settings import AppSettings
from indexer.index import load_index, search_text


class SearchRequest(BaseModel):
    prompt: str


class SearchMatch(BaseModel):
    rank: int
    score: float
    reference: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    matches: list[SearchMatch]


def add_routes(app: FastAPI, app_settings: AppSettings):
    index = (
        app_settings.index
        if isinstance(app_settings.index, IndexFlatIP)
        else load_index(str(app_settings.index))
    )
    retriever = load_retriever()

    @app.post("/api/search")
    async def search(search_request: SearchRequest) -> SearchResponse:
        matches = search_text(
            index=index,
            retriever=retriever,
            text=search_request.prompt,
        )
        matches = [
            SearchMatch(rank=i_match, score=score, reference=str(i_reference), metadata={})
            for i_match, (score, i_reference) in enumerate(matches)
        ]
        return SearchResponse(
            matches=matches,
        )
