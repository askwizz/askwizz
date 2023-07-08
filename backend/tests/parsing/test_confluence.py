import json

from esearch.core.parsing.confluence import create_passages_from_page


def test_confluence_parser(snapshot: str) -> None:
    with open("./tests/fixtures/confluence_page.json") as f:
        page = json.load(f)
    metadata = {
        "atlassian_domain": "bpc-ai.atlassian.net",
        "atlassian_email": "toto@gmail.com",
        "user_id": "user_xnezifgrei",
    }
    passages = create_passages_from_page(page, metadata)
    assert passages == snapshot
