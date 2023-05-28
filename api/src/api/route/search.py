from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from api.settings import AppSettings


class SearchMatch(BaseModel):
    rank: int
    score: float
    reference: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    matches: list[SearchMatch]


def add_routes(app: FastAPI, app_settings: AppSettings):
    @app.post("/api/search")
    async def search() -> SearchResponse:
        return SearchResponse(
            matches=[],
        )
