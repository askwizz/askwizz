import logging
from typing import Literal

from langchain.embeddings.base import Embeddings

EmbeddingModel = Literal["e5"] | Literal["huggingface"]


def load_embedder(model_name: str) -> Embeddings:
    logging.info(f"Loading embedder {model_name}")
    match model_name:
        case "e5":
            from esearch.core.models.embeddings.e5 import E5Basev2

            return E5Basev2()
        case "huggingface":
            from esearch.core.models.embeddings.huggingface import (
                CustomHuggingFaceEmbeddings,
            )

            return CustomHuggingFaceEmbeddings()
        case _:
            raise ValueError(f"Unknown model name: {model_name}")  # noqa: TRY003
