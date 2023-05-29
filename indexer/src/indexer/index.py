from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from indexer.encoder import encode_texts
from indexer.database import Database, PandasDatabase, InMemoryDatabase

INDEX_VECTOR_DIM = 384


def create_index() -> faiss.IndexIDMap:
    raw_index = faiss.IndexFlatIP(INDEX_VECTOR_DIM)
    return faiss.IndexIDMap(raw_index)


def create_database() -> InMemoryDatabase:
    return InMemoryDatabase()


def load_index(file_path: str) -> faiss.IndexIDMap:
    index: faiss.Index = faiss.read_index(file_path)
    if index.d != INDEX_VECTOR_DIM:
        raise ValueError(
            f"Loaded index has wrong dimension, {index.d} but expected"
            f" {INDEX_VECTOR_DIM}"
        )
    return index


def load_database(file_path: str) -> PandasDatabase:
    return PandasDatabase(Path(file_path))


def add_indices_to_database(
    database: Database, ids: np.ndarray[np.int64], texts: list[str]
):
    database.insert_references(ids, texts)


def ingest_texts(
    index: faiss.IndexIDMap,
    database: Database,
    retriever: SentenceTransformer,
    texts: list[str],
    batch_size: int,
):
    embeddings = encode_texts(retriever=retriever, texts=texts, batch_size=batch_size)
    index_size = index.ntotal
    ids = np.arange(index_size, len(texts) + index_size, dtype=np.int64)

    index.add_with_ids(embeddings, ids)
    add_indices_to_database(database, ids, texts)


def search_text(
    index: faiss.IndexIDMap,
    retriever: SentenceTransformer,
    text: str,
):
    embedding = retriever.encode(
        sentences=[text],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    result_scores, result_indices = index.search(embedding, max(5, index.ntotal))
    return list(zip(result_scores[0], result_indices[0]))
