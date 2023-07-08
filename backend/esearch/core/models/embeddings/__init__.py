import logging
from typing import Literal

from esearch.core.models.embeddings.e5 import CustomEmbeddings

EmbeddingModel = Literal["e5"] | Literal["huggingface"]


def load_embedder(model_name: str) -> CustomEmbeddings:
    logging.info(f"Loading embedder {model_name}")
    match model_name:
        case "e5":
            from esearch.core.models.embeddings.e5 import E5v2

            return E5v2()
        case "huggingface":
            from esearch.core.models.embeddings.huggingface import (
                CustomHuggingFaceEmbeddings,
            )

            return CustomHuggingFaceEmbeddings()  # type: ignore
        case _:
            raise ValueError(f"Unknown model name: {model_name}")
