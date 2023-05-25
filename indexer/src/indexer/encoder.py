from typing import cast

import numpy as np
from sentence_transformers import SentenceTransformer


def load_retriever(device: str | None = None) -> SentenceTransformer:
    return SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", device=device)


def encode_texts(
    retriever: SentenceTransformer,
    texts: list[str],
    batch_size: int,
    device: str | None = None,
    show_progress_bar: bool = False,
) -> np.ndarray:
    """Encode text to embeddings"""
    embeddings = retriever.encode(
        sentences=texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        batch_size=batch_size,
        device=device or "cpu",
        show_progress_bar=show_progress_bar,
    )
    embeddings = cast(np.ndarray, embeddings)
    return embeddings
