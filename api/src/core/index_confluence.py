import requests
from api.lifespan import ml_models
from langchain.docstore.document import Document
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
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


def get_confluence_pages(
    wiki_url: str, email: str, token: str, space_key: str, page_ids: list[str]
) -> list[Document]:
    loader = ConfluenceLoader(url=wiki_url, username=email, api_key=token)
    documents = loader.load(
        space_key=space_key, page_ids=page_ids, include_attachments=False, limit=50
    )
    return documents[: len(documents) // 2]


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )


def get_confluence_pages_from_space(
    space: str, wiki_url: str, email: str, token: str
) -> list[Document]:
    page_ids = get_page_ids_from_space(space, wiki_url, email, token)
    return get_confluence_pages(wiki_url, email, token, space, page_ids)


def index_confluence(space: str, wiki_url: str, email: str, token: str) -> None:
    """Ingest confluence space into a database.
    poetry run python -m indexer.cli ingest_confluence \
            --space "TW" \
            --wiki_url "https://bpc-ai.atlassian.net/wiki" \
            --email "maximeduvalsy@gmail.com" \
            --token ""
    """
    print("Ingesting confluence space into vector database...")
    page_ids = get_page_ids_from_space(space, wiki_url, email, token)
    print("Got page ids.")
    confluence_pages = get_confluence_pages(wiki_url, email, token, space, page_ids)
    print("Extracted documents.")

    text_splitter = get_text_splitter()
    confluence_chunks = text_splitter.split_documents(confluence_pages)
    print("Split documents.")

    Milvus.from_documents(
        confluence_chunks,
        ml_models["embedder"],
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name=get_collection_name_from_space_key(space),
        drop_old=True,
    )
    print("Embedded documents.")
