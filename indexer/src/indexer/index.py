from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

from indexer.encoder import encode_texts

INDEX_VECTOR_DIM = 384
INDEX_TYPE = faiss.IndexFlatIP


def create_index() -> INDEX_TYPE:
    return faiss.IndexFlatIP(INDEX_VECTOR_DIM)


def load_index(file_path: str) -> INDEX_TYPE:
    index: faiss.Index = faiss.read_index(file_path)
    if index.d != INDEX_VECTOR_DIM:
        raise ValueError(
            f"Loaded index has wrong dimension, {index.d} but expected"
            f" {INDEX_VECTOR_DIM}"
        )
    return index


def ingest_texts(
    index: INDEX_TYPE,
    retriever: SentenceTransformer,
    texts: list[str],
    batch_size: int,
):
    embeddings = encode_texts(retriever=retriever, texts=texts, batch_size=batch_size)
    index.add(embeddings)  # type: ignore


def search_text(
    index: INDEX_TYPE,
    retriever: SentenceTransformer,
    text: str,
):
    embedding = retriever.encode(
        sentences=[text],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    result_scores, result_indices = index.search(embedding, 5)
    return list(zip(result_scores[0], result_indices[0]))
