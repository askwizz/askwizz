from typing import List, Literal

from pydantic import BaseModel


class ReceivedMessage(BaseModel):
    kind: Literal["QUERY", "AUTH"]
    message: str


class QueryMessage(BaseModel):
    texts: List[str]
    query: str


class SentMessage(BaseModel):
    kind: Literal["CLEAR", "ANSWER", "ANSWER_STOP"]
    message: str
