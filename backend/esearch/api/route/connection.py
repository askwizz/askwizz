import logging
from typing import Annotated, List

from fastapi import BackgroundTasks, Depends, FastAPI
from sqlalchemy.orm import Session

from esearch.api.authorization import (
    UserData,
    get_current_user,
)
from esearch.api.exceptions import DBNotInitializedException
from esearch.api.lifespan import ml_models
from esearch.api.settings import AppSettings
from esearch.core.connection.definition import Connection
from esearch.core.connection.entity import (
    NewConnectionPayload,
    create_or_update_connection,
    delete_connection,
)
from esearch.core.connection.index import index_connection
from esearch.db.engine import get_db
from esearch.db.models.connection import fetch_connections_of_user
from esearch.services.milvus.client import Milvus, milvus_dependency


def add_routes(app: FastAPI, settings: AppSettings) -> None:
    @app.post("/api/new-connection")
    async def new_connection(
        connection_data: NewConnectionPayload,
        user_data: Annotated[UserData, Depends(get_current_user)],
        background_tasks: BackgroundTasks,
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
        milvus_client: Annotated[Milvus, Depends(milvus_dependency)],
    ) -> None:
        logging.info("New connection request")
        if db is None:
            raise DBNotInitializedException()
        logging.info("Creating connection")
        connection = create_or_update_connection(db, connection_data, user_data.user_id)
        logging.info(f"Created connection {connection.id_}")
        background_tasks.add_task(
            index_connection, connection, ml_models["embedder"], db, milvus_client
        )

    @app.get("/api/connections")
    async def connections(
        user_data: Annotated[UserData, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
    ) -> List[Connection]:
        if db is None:
            raise DBNotInitializedException()

        return fetch_connections_of_user(db, user_data.user_id)

    @app.delete("/api/connections/{connection_id}")
    async def delete_connections(
        connection_id: str,
        user_data: Annotated[UserData, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db(settings.sqlalchemy_database_url))],
        milvus_client: Annotated[Milvus, Depends(milvus_dependency)],
    ) -> None:
        if db is None:
            raise DBNotInitializedException()

        delete_connection(db, user_data.user_id, connection_id, milvus_client)
