from pydantic import BaseModel

from esearch.core.passage.definition import PassageMetadata


class RetrievedPassage(BaseModel):
    metadata: PassageMetadata
    score: float
    passage_id: int
    text: str | None = None
