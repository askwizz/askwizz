import click
import faiss
import torch
from sentence_transformers import SentenceTransformer

from indexer.encoder import load_retriever
from indexer.index import load_index, search_text


@click.command("search")
@click.argument(
    "search_prompt",
    type=str,
)
@click.option(
    "--index-file-path",
    type=click.Path(dir_okay=False, exists=True),
    required=True,
)
@click.option(
    "--cuda",
    type=bool,
    is_flag=True,
)
def search_command(
    search_prompt: str,
    index_file_path: str,
    cuda: bool,
):
    """Search for input strings in index file."""
    if cuda and not torch.cuda.is_available():
        raise Exception("Can't use CUDA as it is not supported.")
    device = "cuda" if cuda else None

    # load components
    index: faiss.IndexFlatIP = load_index(index_file_path)
    retriever: SentenceTransformer = load_retriever(device=device)

    # search index
    results = search_text(
        index=index,
        retriever=retriever,
        text=search_prompt,
    )

    for result_score, result_index in results:
        print(f"result_score={result_score},result_index={result_index}")
