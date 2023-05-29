from typing import Generator
from indexer.database import Database

import pytest
from faiss import IndexIDMap
from indexer.encoder import load_retriever
from indexer.index import create_index, ingest_texts, create_database
from starlette.testclient import TestClient

from api.app import create_app_with_settings
from api.route.search import SearchResponse
from api.settings import AppSettings, OAuthConfig


@pytest.fixture
def database() -> Generator[Database, None, None]:
    yield create_database()


@pytest.fixture
def index(database: Database) -> Generator[IndexIDMap, None, None]:
    index = create_index()
    sentences = [
        "The house is brown.",
        "The sky is blue.",
        "Apples are red.",
        "I'm in love with you",
    ]
    retriever = load_retriever()
    ingest_texts(
        index=index,
        database=database,
        retriever=retriever,
        texts=sentences,
        batch_size=32,
    )

    yield index


@pytest.fixture
def client(index: IndexIDMap, database: Database) -> Generator[TestClient, None, None]:
    app_settings = AppSettings(
        oauth_atlassian=OAuthConfig(client_id="", client_secret=""),
        index=index,
        database=database,
    )
    app = create_app_with_settings(app_settings=app_settings)
    client = TestClient(app=app)
    yield client


def test_search(client: TestClient):
    response = client.post(
        url="/api/search",
        json={"prompt": "What color is the sky?"},
    )
    assert response.status_code == 200
    search_response = SearchResponse.parse_obj(response.json())
    assert len(search_response.matches) >= 1
    assert search_response.matches[0].reference == "The sky is blue."
