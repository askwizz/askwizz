from typing import Generator

import pytest
from fastapi.testclient import TestClient

from api.app import create_app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app = create_app()
    client = TestClient(app=app)
    yield client


def test_search(client: TestClient):
    response = client.post(
        url="/api/search",
        json={},
    )
    assert response.status_code == 200
    assert response.json() == {"matches": []}
