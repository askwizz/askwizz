from typing import Any
from faiss import IndexIDMap

from fastapi import FastAPI
from indexer.encoder import load_retriever
from indexer.database import Database
from pydantic import BaseModel

from api.settings import AppSettings
from indexer.index import load_database, load_index, search_text


class SearchRequest(BaseModel):
    prompt: str


class SearchMatch(BaseModel):
    rank: int
    score: float
    reference: str
    metadata: dict[str, Any]
    index: int


class SearchResponse(BaseModel):
    matches: list[SearchMatch]


def add_routes(app: FastAPI, app_settings: AppSettings):
    index = (
        app_settings.index
        if isinstance(app_settings.index, IndexIDMap)
        else load_index(str(app_settings.index))
    )
    database = (
        app_settings.database
        if isinstance(app_settings.database, Database)
        else load_database(str(app_settings.database))
    )
    retriever = load_retriever()

    @app.post("/api/search")
    async def search(search_request: SearchRequest) -> SearchResponse:
        matches = search_text(
            index=index,
            retriever=retriever,
            text=search_request.prompt,
        )
        matches = [v for v in matches if not v[1] == -1]
        references = database.find_references(
            [i_ref for (_, i_ref) in matches if not i_ref == -1]
        )
        matches = [
            SearchMatch(
                rank=i_match,
                score=score,
                reference=references[i_reference],
                index=i_reference,
                metadata={},
            )
            for i_match, (score, i_reference) in enumerate(matches)
        ]
        return SearchResponse(
            matches=matches,
        )
