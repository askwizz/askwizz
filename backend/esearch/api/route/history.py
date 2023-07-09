from typing import Annotated, List

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.api.authorization import (
    UserData,
    get_current_user,
    throw_if_not_authenticated,
)
from esearch.api.settings import AppSettings
from esearch.core.search import get_search_history
from esearch.core.search_history.definition import SearchHistory
from esearch.db.engine import get_db


class SearchHistoryResponse(BaseModel):
    searches: List[SearchHistory]


def add_routes(app: FastAPI, settings: AppSettings) -> None:
    @app.get("/api/history/search")
    async def search_history(
        user_data: Annotated[UserData, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
    ) -> SearchHistoryResponse:
        throw_if_not_authenticated(user_data)
        searches = get_search_history(db, user_data.user_id)
        return SearchHistoryResponse(searches=searches)
