from core.index_confluence import index_confluence
from fastapi import FastAPI
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
    async def index(request: IndexRequest) -> IndexResponse:
        index_confluence(
            request.space_key,
            request.wiki_url,
            request.atlassian_email,
            request.atlassian_token,
        )
