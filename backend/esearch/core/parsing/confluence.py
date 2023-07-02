import itertools
import json
from typing import Iterable, List
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

TEXT_SPLITTERS = [
    RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )
]


class ConfluenceChunk(BaseModel):
    text: str
    relative_path: str | None


def is_element_header(el: Tag) -> bool:
    return el.name.startswith("h")


def parse_confluence_html(raw_html: str) -> BeautifulSoup:
    return BeautifulSoup(raw_html, "lxml")


def format_header_text(header: str | None) -> str:
    if header is None:
        return ""
    return quote(header.replace(" ", "-"))


def create_chunks_from_element(elements: Iterable[Tag]) -> List[ConfluenceChunk]:
    chunks: List[ConfluenceChunk] = []
    current_header = None
    min_chunk_size = 20
    for element in elements:
        text_element = element.get_text()
        if is_element_header(element):
            current_header = text_element
            continue
        if not text_element or len(text_element) < min_chunk_size:
            continue
        chunks.append(
            ConfluenceChunk(
                text=element.get_text(),
                relative_path=format_header_text(current_header),
            )
        )
    return chunks


def create_chunks_from_html(html: BeautifulSoup) -> List[ConfluenceChunk]:
    body = html.body
    if not body:
        return []
    page_elements: Iterable[Tag] = body.children  # type: ignore
    return create_chunks_from_element(page_elements)


def create_documents_from_page(page: Document) -> List[Document]:
    title = page.metadata["title"]
    page_id = page.metadata["id"]
    page_path = page.metadata["path"]
    base_metadata = {"page_id": page_id, "page_path": page_path, "title": title}
    html = parse_confluence_html(page.page_content)
    chunks = create_chunks_from_html(html)
    chunk_documents = [
        Document(
            page_content=chunk.text,
            metadata={**base_metadata, "relative_path": chunk.relative_path},
        )
        for chunk in chunks
    ]
    return list(
        itertools.chain.from_iterable(
            [splitters.split_documents(chunk_documents) for splitters in TEXT_SPLITTERS]
        )
    )


def create_documents_from_pages(pages: list) -> List[Document]:
    return list(
        itertools.chain.from_iterable(
            [create_documents_from_page(page) for page in pages]
        )
    )


if __name__ == "__main__":
    with open("./pages.json") as f:
        pages = json.load(f)
    page_documents = [
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
    documents = create_documents_from_pages(pages)
    print(documents)
