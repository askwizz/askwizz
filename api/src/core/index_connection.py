import json
from typing import List

import requests
import tqdm
from api.lifespan import ml_models
from core.create_connection import ConnectionEntity
from core.index_confluence import (
    get_collection_name_from_connection,
    get_confluence_pages_from_space,
    get_text_splitter,
)
from langchain.vectorstores import Milvus
from requests.auth import HTTPBasicAuth

from db.models.connection import ConnectionStatus


def list_confluence_space_keys(connection: ConnectionEntity) -> List[str]:
    url = f"https://{connection.domain}/wiki/api/v2/spaces"
    auth = HTTPBasicAuth(connection.atlassian_email, connection.atlassian_token)
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, auth=auth)
    if response.status_code != 200:
        raise Exception("Could not get space keys from confluence space")
    json_response = json.loads(response.text)
    print("Got response", json_response)
    return [result["key"] for result in json_response.get("results", [])]


def index_confluence_connection(connection: ConnectionEntity) -> None:
    space_keys = list_confluence_space_keys(connection)
    text_splitter = get_text_splitter()
    collection_name = get_collection_name_from_connection(connection.name)

    for space_key in tqdm.tqdm(space_keys):
        space_pages = get_confluence_pages_from_space(
            space_key,
            f"https://{connection.domain}/wiki",
            connection.atlassian_email,
            connection.atlassian_token,
        )
        space_chunks = text_splitter.split_documents(space_pages)
        Milvus.from_documents(
            space_chunks,
            ml_models["embedder"],
            connection_args={"host": "127.0.0.1", "port": "19530"},
            collection_name=collection_name,
            drop_old=True,
        )


def index_connection(connection: ConnectionEntity) -> None:
    print(connection)
    if connection.status != ConnectionStatus.Creating.value:  # type: ignore
        return
    index_confluence_connection(connection)
