import copy
import datetime
import json
from datetime import timezone
from typing import Any, Generator, Iterable, List, Tuple
from urllib.parse import quote

from atlassian import Confluence
from bs4 import BeautifulSoup, Tag
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

from esearch.core.parsing.helpers import get_generator_packer, unpack_generator
from esearch.core.passage.definition import (
    ConfluenceDocumentReference,
    DocumentReference,
    DocumentType,
    Passage,
    PassageMetadata,
)

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
    header: str


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
                header=current_header or "",
            )
        )
    return chunks


def create_chunks_from_html(html: BeautifulSoup) -> List[ConfluenceChunk]:
    body = html.body
    if not body:
        return []
    page_elements: Iterable[Tag] = body.children  # type: ignore
    return create_chunks_from_element(page_elements)


def get_confluence_passage_title(doc: Document, page: dict) -> str:
    page_title = page["title"]
    space_key = page["space"]
    header = doc.metadata["header"]
    start_index = doc.metadata["start_index"]
    end_index = doc.metadata["end_index"]
    size = end_index - start_index
    return (
        f"Space: {space_key} | Page: {page_title} | Section: {header} |"
        f"Start: {start_index} | Size: {size}"
    )


def get_documents_from_html(html: BeautifulSoup) -> List[Document]:
    chunks = create_chunks_from_html(html)
    documents_from_raw_chunks = [
        Document(
            page_content=chunk.text,
            metadata={"path": chunk.relative_path, "header": chunk.header},
        )
        for chunk in chunks
    ]
    documents_with_reference: List[Document] = []
    for doc in documents_from_raw_chunks:
        for splitter in TEXT_SPLITTERS:
            for chunk in splitter.split_text(doc.page_content):
                start_index = doc.page_content.find(chunk)
                documents_with_reference.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            **copy.deepcopy(doc.metadata),
                            "start_index": start_index,
                            "end_index": start_index + len(chunk),
                        },
                    )
                )
    return documents_with_reference


def create_passages_from_page(page: dict, metadata: dict) -> List[Passage]:
    atlassian_domain = metadata["atlassian_domain"]
    atlassian_email = metadata["atlassian_email"]
    user_id = metadata["user_id"]

    indexed_at = str(datetime.datetime.now(timezone.utc))

    page_path = page["_links"]["webui"]
    page_link = f"https://{atlassian_domain}/wiki{page_path}"
    page_creation_date = page["history"]["createdDate"]

    html = parse_confluence_html(page["body"]["storage"]["value"])
    documents_with_reference = get_documents_from_html(html)

    return [
        Passage(
            text=doc.page_content,
            metadata=PassageMetadata(
                title=get_confluence_passage_title(doc, page),
                indexed_at=str(indexed_at),
                created_at=page_creation_date,
                last_update=page["version"]["when"],
                creator=page["history"]["createdBy"]["displayName"],
                link=f"{page_link}#{doc.metadata['path']}",
                document_link=page_link,
                reference=DocumentReference(
                    confluence=ConfluenceDocumentReference(
                        domain=atlassian_domain,
                        page_path=page_path,
                        chunk_id=doc.metadata["path"],
                        start_index=doc.metadata["start_index"],
                        end_index=doc.metadata["end_index"],
                        space_key=page["space"],
                    )
                ),
                filetype=DocumentType.CONFLUENCE,
                connection_id=user_id,
                indexor=atlassian_email,
            ),
        )
        for doc in documents_with_reference
    ]


def create_passages_from_pages(
    pages_generator: Generator[Tuple[List[dict], int], None, None], metadata: dict
) -> Generator[Tuple[Passage, int], None, None]:
    return unpack_generator(
        (
            (create_passages_from_page(page, metadata), page_count)
            for pages, page_count in pages_generator
            for page in pages
        )
    )


def confluence_pages_from_space(
    confluence: Confluence,
    space_key: str,
    start: int,
    limit: int,
    **kwargs: Any,  # noqa: ANN401
) -> List[dict]:
    space_pages = confluence.get_all_pages_from_space(
        space_key, start=start, limit=limit, **kwargs
    )
    return [{"space": space_key, **page} for page in space_pages]


def confluence_pages_generator(
    atlassian_domain: str, email: str, token: str
) -> Generator[Tuple[List[dict], int], None, None]:
    confluence = Confluence(
        url=f"https://{atlassian_domain}", username=email, password=token, cloud=True
    )
    spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
    if not spaces:
        yield [], 0
    space_results: List[Any] = spaces["results"]  # type: ignore
    constant_query_params = {
        "status": None,
        "expand": "body.storage,version,history",
        "content_type": "page",
    }
    pages_count = 0
    for space in space_results:
        start = 0
        limit = 100
        space_pages = confluence_pages_from_space(
            confluence, space["key"], start=0, limit=limit, **constant_query_params
        )
        pages_count += len(space_pages)
        yield space_pages, pages_count
        while len(space_pages) > 0:
            start += limit
            space_pages = confluence_pages_from_space(
                confluence,
                space["key"],
                start=start,
                limit=limit,
                **constant_query_params,
            )
            pages_count += len(space_pages)
            yield space_pages, pages_count


def get_confluence_passages_generator(
    user_id: str, atlassian_domain: str, email: str, token: str
) -> Generator[Tuple[List[Passage], int], None, None]:
    pages_generator = confluence_pages_generator(atlassian_domain, email, token)
    metadata = {
        "atlassian_domain": atlassian_domain,
        "atlassian_email": email,
        "atlassian_token": token,
        "user_id": user_id,
    }
    generator_packer = get_generator_packer(1024)
    return generator_packer(create_passages_from_pages(pages_generator, metadata))


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
    documents = create_passages_from_pages(
        pages,
        {
            "atlassian_domain": "bpc-ai.atlassian.net",
            "atlassian_email": "maximeduvalsy@gmail.com",
            "user_id": "xxxxxxxx__toto",
        },
    )
    print(documents)
