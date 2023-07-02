from typing import Any, List

import requests
from atlassian import Confluence
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from requests.auth import HTTPBasicAuth


def get_collection_name_from_space_key(space_key: str) -> str:
    return f"{space_key}Collection"


def get_collection_name_from_connection(connection_name: str) -> str:
    return f"Collection_connection_{connection_name}"


def get_page_ids_from_space(space: str, wiki_url: str, email: str, token: str) -> list:
    parse_space_url = (
        f"{wiki_url}/rest/api/space/{space}/content?start=0&limit=500&type=page"
    )
    headers = {"Content-Type": "application/json;charset=iso-8859-1"}
    auth = HTTPBasicAuth(email, token)
    response = requests.get(parse_space_url, headers=headers, auth=auth)
    pages = response.json()["page"]["results"]
    return [p["id"] for p in pages]


def get_confluence_pages(domain: str, email: str, token: str) -> list[Document]:
    confluence = Confluence(
        url=f"https://{domain}", username=email, password=token, cloud=True
    )
    spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
    if not spaces:
        return []
    space_results: List[Any] = spaces["results"]  # type: ignore
    pages = []
    for space in space_results:
        space_pages = confluence.get_all_pages_from_space(
            space["key"],
            start=0,
            limit=100,
            status=None,
            expand="body.storage,version",
            content_type="page",
        )
        pages.extend(space_pages)
    return [
        Document(
            page_content=page["body"]["storage"]["value"],
            metadata={
                "title": page["title"],
                "id": page["id"],
                "path": page["_links"]["webui"],
            },
        )
        for page in pages
    ]


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )


def get_confluence_pages_from_domain(
    domain: str, email: str, token: str
) -> list[Document]:
    return get_confluence_pages(domain, email, token)
