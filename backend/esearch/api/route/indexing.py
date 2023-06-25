from typing import Annotated

from esearch.api.authorization import TokenData, get_current_user
from esearch.core.index_confluence import index_confluence
from fastapi import Depends, FastAPI
from pydantic import BaseModel


class IndexRequest(BaseModel):
    space_key: str  # TW
    wiki_url: str  # https://bpc-ai.atlassian.net/wiki
    atlassian_email: str  # maximeduvalsy@gmail.com
    atlassian_token: str


def add_routes(app: FastAPI) -> None:
    @app.post("/api/index")
    async def index(
        index_request: IndexRequest,
        token: Annotated[TokenData, Depends(get_current_user)],
    ) -> None:
        index_confluence(
            index_request.space_key,
            index_request.wiki_url,
            index_request.atlassian_email,
            index_request.atlassian_token,
        )
