import os
from pathlib import Path
import sys

import click
import faiss
import torch
from sentence_transformers import SentenceTransformer

from indexer.encoder import load_retriever
from indexer.index import create_index, ingest_texts, load_index, load_database
from indexer.database import Database


@click.command("ingest")
@click.option(
    "--index-file-path",
    type=click.Path(dir_okay=False),
    required=True,
)
@click.option(
    "--cuda",
    type=bool,
    is_flag=True,
)
@click.option(
    "--batch-size",
    type=int,
    default=32,
)
@click.option(
    "--text",
    type=str,
)
def ingest_command(
    index_file_path: str,
    cuda: bool,
    batch_size: int,
    text: str | None,
):
    """Ingest input strings into index file."""
    if cuda and not torch.cuda.is_available():
        raise Exception("Can't use CUDA as it is not supported.")
    device = "cuda" if cuda else None

    # load components
    index: faiss.IndexIDMap = (
        load_index(index_file_path)
        if os.path.exists(index_file_path)
        else create_index()
    )

    database_path = str(Path(index_file_path).with_suffix(".csv"))
    database: Database = load_database(database_path)
    retriever: SentenceTransformer = load_retriever(device=device)

    # encode texts
    if text is None:
        text = sys.stdin.read()
    texts = text.split("\n\n")

    # add to index
    ingest_texts(
        index=index,
        database=database,
        retriever=retriever,
        texts=texts,
        batch_size=batch_size,
    )

    # save index
    faiss.write_index(index, index_file_path)
