import json
import logging
from typing import Any, Callable, Coroutine

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from esearch.api.authorization import (
    CredentialsException,
    get_current_user,
)
from esearch.api.lifespan import ML_MODELS
from esearch.api.settings import AppSettings
from esearch.core.answer import provide_answers
from esearch.core.messages import QueryMessage, ReceivedMessage, SentMessage


class AnswerRequest(BaseModel):
    query: str
    texts: list[str]


async def write_message(websocket: WebSocket, message: SentMessage) -> None:
    await websocket.send_text(json.dumps(message.dict()))


def get_callback(websocket: WebSocket) -> Callable[[str], Coroutine[Any, Any, None]]:
    async def callback(message: str) -> None:
        await write_message(websocket, SentMessage(kind="ANSWER", message=message))

    return callback


def add_routes(app: FastAPI, settings: AppSettings) -> None:
    @app.websocket("/api/answer/ws")
    async def answer_route(
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()
        is_authenticated = False
        llm = ML_MODELS["llm"]
        while True:
            raw_data = await websocket.receive_text()
            data = ReceivedMessage(**json.loads(raw_data))
            if data.kind == "AUTH":
                get_current_user(data.message, settings)
                is_authenticated = True
            if not is_authenticated:
                raise CredentialsException
            if data.kind == "QUERY":
                logging.info("Providing answer to query")
                callback = get_callback(websocket)
                parsed_message = QueryMessage(**json.loads(data.message))
                await provide_answers(llm, parsed_message, callback)
