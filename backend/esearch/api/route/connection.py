from typing import Annotated, List

from fastapi import BackgroundTasks, Depends, FastAPI
from sqlalchemy.orm import Session

from esearch.api.authorization import UserData, get_current_user
from esearch.api.exceptions import DBNotInitializedException, NotAuthenticatedException
from esearch.api.lifespan import ml_models
from esearch.api.settings import AppSettings
from esearch.core.connection.definition import Connection
from esearch.core.connection.entity import (
    NewConnectionPayload,
    create_connection,
    delete_connection,
)
from esearch.core.connection.index import index_connection
from esearch.db.engine import get_db
from esearch.db.models.connection import fetch_connections_of_user


def add_routes(app: FastAPI, settings: AppSettings) -> None:
    @app.post("/api/new-connection")
    async def new_connection(
        connection_data: NewConnectionPayload,
        user: Annotated[UserData, Depends(get_current_user)],
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db(settings.sqlalchemy_database_url)),  # noqa: B008
    ) -> None:
        if user.user_id is None:
            raise NotAuthenticatedException()
        if db is None:
            raise DBNotInitializedException()
        connection = create_connection(db, connection_data, user.user_id)
        background_tasks.add_task(
            index_connection, connection, ml_models["embedder"], db
        )

    @app.get("/api/connections")
    async def connections(
        token_data: Annotated[UserData, Depends(get_current_user)],
        db: Session = Depends(get_db(settings.sqlalchemy_database_url)),  # noqa: B008
    ) -> List[Connection]:
        if token_data.user_id is None:
            raise NotAuthenticatedException()
        if db is None:
            raise DBNotInitializedException()

        return fetch_connections_of_user(db, token_data.user_id)

    @app.delete("/api/connections/{connection_id}")
    async def delete_connections(
        connection_id: str,
        token_data: Annotated[UserData, Depends(get_current_user)],
        db: Session = Depends(get_db(settings.sqlalchemy_database_url)),  # noqa: B008
    ) -> None:
        if token_data.user_id is None:
            raise NotAuthenticatedException()
        if db is None:
            raise DBNotInitializedException()

        delete_connection(db, token_data.user_id, connection_id)
