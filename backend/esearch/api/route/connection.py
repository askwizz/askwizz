from typing import Annotated, List

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.api.authorization import TokenData, get_current_user
from esearch.core.connection import (
    ConnectionEntity,
    create_connection,
    delete_connection,
    fetch_connections_of_user,
)
from esearch.core.index_connection import index_connection
from esearch.db.engine import get_db
from esearch.db.models.connection import ConnectionCreate


class Connection(BaseModel):
    name: str
    email: str
    token: str
    domain: str


def add_routes(app: FastAPI) -> None:
    @app.post("/api/new-connection")
    async def new_connection(
        connection_data: Connection,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),  # noqa: B008
    ) -> None:
        if token_data.user_id is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if db is None:
            raise HTTPException(status_code=401, detail="Database not connected")

        connection = create_connection(
            db,
            ConnectionCreate(
                atlassian_email=connection_data.email,
                atlassian_token=connection_data.token,
                domain=connection_data.domain,
                name=connection_data.name,
                user_id=token_data.user_id,
            ),
        )
        background_tasks.add_task(index_connection, connection)

    @app.get("/api/connections")
    async def connections(
        token_data: Annotated[TokenData, Depends(get_current_user)],
        db: Session = Depends(get_db),  # noqa: B008
    ) -> List[ConnectionEntity]:
        if token_data.user_id is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if db is None:
            raise HTTPException(status_code=401, detail="Database not connected")

        return fetch_connections_of_user(db, token_data.user_id)

    @app.delete("/api/connections/{connection_id}")
    async def delete_connections(
        connection_id: str,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        db: Session = Depends(get_db),  # noqa: B008
    ) -> None:
        if token_data.user_id is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if db is None:
            raise HTTPException(status_code=401, detail="Database not connected")

        delete_connection(db, token_data.user_id, connection_id)
