from typing import Annotated

from api.authorization import get_current_user
from core.index_confluence import index_confluence
from fastapi import Depends, FastAPI
from pydantic import BaseModel


class IndexRequest(BaseModel):
    space_key: str  # TW
    wiki_url: str  # https://bpc-ai.atlassian.net/wiki
    atlassian_email: str  # maximeduvalsy@gmail.com
    atlassian_token: str


class IndexResponse(BaseModel):
    n_pages: int
    n_documents: int


def add_routes(app: FastAPI) -> None:
    @app.post("/api/index")
    async def index(
        index_request: Annotated[IndexRequest, Depends(get_current_user)]
    ) -> IndexResponse:
        index_confluence(
            index_request.space_key,
            index_request.wiki_url,
            index_request.atlassian_email,
            index_request.atlassian_token,
        )

        return IndexResponse(n_pages=0, n_documents=0)
