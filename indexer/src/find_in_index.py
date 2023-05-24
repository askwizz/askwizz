import os

import faiss
import numpy as np
import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"


def load_data():
    df = load_dataset("squad", split="train").to_pandas()
    df = df[["title", "context"]]
    df = df.drop_duplicates(subset="context")
    return df


df = load_data()


def get_faiss_index(name: str) -> faiss.IndexFlatIP:
    if not os.path.exists(name):
        raise Exception("Index does not exist")
    return faiss.read_index("test.index")


def load_sentence_embedder():
    return SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", device=device)


def encode_question(question: str, retriever: any) -> np.ndarray:
    embedding = retriever.encode([question])
    return embedding / embedding.sum(axis=1, keepdims=True)


def print_top_answers(retriever, index, question, k=3):
    question_embedding = encode_question(question, retriever)
    scores, indices = index.search(question_embedding, k=k)
    for score, index in zip(scores[0], indices[0]):
        print(f"Score: {score}")
        print(df.iloc[index]["context"])
        print()


def main():
    index_name = "full.index"
    index = get_faiss_index(index_name)
    top_k = 5

    retriever = load_sentence_embedder()
    query = "What is the black death ?"
    print_top_answers(retriever, index, query, k=top_k)


if __name__ == "__main__":
    main()
