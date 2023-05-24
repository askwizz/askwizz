import os

import numpy as np
from tqdm.auto import tqdm
import torch
import faiss
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

from constants import VECTOR_DIM


device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loaded all dependencies")


def get_faiss_index(name: str) -> faiss.IndexFlatIP:
    if os.path.exists(name):
        print("Found existing index, loading...")
        return faiss.read_index("test.index")
    return faiss.IndexFlatIP(VECTOR_DIM)


def load_sentence_embedder():
    return SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", device=device)


def encode_texts(texts: list[str], retriever: any) -> np.ndarray:
    embeddings = retriever.encode(texts)
    return embeddings / embeddings.sum(axis=1, keepdims=True)


def load_data():
    df = load_dataset("squad", split="train").to_pandas()
    df = df[["title", "context"]]
    df = df.drop_duplicates(subset="context")
    return df


def encode_data(retriever, index):
    df = load_data()
    batch_size = 128
    total_size = len(df)
    for i in tqdm(range(0, total_size, batch_size)):
        i_end = min(i + batch_size, len(df))
        batch = df.iloc[i:i_end]
        embeddings = encode_texts(batch["context"].tolist(), retriever)
        index.add(embeddings)


def main():
    index_name = "full.index"
    index = get_faiss_index(index_name)
    index.reset()
    print(f"Index contains {index.ntotal} vectors")
    retriever = load_sentence_embedder()
    print("Loaded retriever")

    encode_data(retriever, index)
    print("Encoding data")
    faiss.write_index(index, index_name)


if __name__ == "__main__":
    main()
