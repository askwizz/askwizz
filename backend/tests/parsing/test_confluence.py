import json

from esearch.core.parsing.confluence import create_passages_from_page
from esearch.core.passage.definition import Passage, PassageMetadata


def remove_date(passage: Passage) -> Passage:
    return Passage(
        **{
            **passage.dict(),
            "metadata": PassageMetadata(
                **{**passage.metadata.dict(), "indexed_at": "2022-10-10"}
            ),
        }
    )


def test_confluence_parser(snapshot: str) -> None:
    with open("./tests/fixtures/confluence_page.json") as f:
        page = json.load(f)
    metadata = {
        "atlassian_domain": "bpc-ai.atlassian.net",
        "atlassian_email": "toto@gmail.com",
        "connection_id": "conn_xnezifgrei",
    }
    passages = create_passages_from_page(page, metadata)
    passages_without_date = [remove_date(p) for p in passages]
    assert passages_without_date == snapshot
