import re

from atlassian import Confluence
from pydantic import BaseModel
from sqlalchemy.orm import Session

from esearch.core.connection.definition import (
    AtlassianData,
    Connection,
    ConnectionSource,
)
from esearch.core.parsing.confluence import create_passages_from_page
from esearch.db.models.connection import fetch_connection_of_user


class ConfluencePassageTextPayload(BaseModel):
    passage_hash: str
    page_path: str


class PassageTextPayload(BaseModel):
    confluence: ConfluencePassageTextPayload | None = None


def get_confluence_text(
    connection: Connection,
    connection_id: str,
    passage_hash: str,
    page_path: str,
) -> str:
    atlassian_configuration: AtlassianData = connection.configuration.atlassian  # type: ignore  # noqa: E501
    confluence = Confluence(
        url=f"https://{atlassian_configuration.atlassian_domain}",
        username=atlassian_configuration.atlassian_email,
        password=atlassian_configuration.atlassian_token,
        cloud=True,
    )
    page_id_result = re.search("(?<=pages\/)\d*(?=\/)", page_path)
    space_key_result = re.search("(?<=spaces\/)[a-zA-Z]*(?=\/pages)", page_path)
    if page_id_result is None:
        raise Exception("Passage not found")
    if space_key_result is None:
        raise Exception("Passage not found")
    page_id = page_id_result.group(0)
    space_key = space_key_result.group(0)
    page: dict = confluence.get_page_by_id(page_id, expand="body.storage,version,history")  # type: ignore  # noqa: E501
    page["space"] = space_key
    if not page:
        raise Exception("Passage not found")
    metadata = {
        "atlassian_domain": atlassian_configuration.atlassian_domain,
        "atlassian_email": atlassian_configuration.atlassian_email,
        "connection_id": connection_id,
    }
    passages = create_passages_from_page((page), metadata)
    text = ""
    for p in passages:
        if p.metadata.reference.text_hash == passage_hash:
            text = p.text
            break
    if not text:
        raise Exception("Passage not found")
    return text


def get_passage_text(
    db: Session,
    user_id: str,
    connection_id: str,
    config: PassageTextPayload,
) -> str:
    connection = fetch_connection_of_user(db, user_id, connection_id)
    if connection.source == ConnectionSource.CONFLUENCE:
        confluence_config: ConfluencePassageTextPayload = config.confluence  # type: ignore
        return get_confluence_text(
            connection,
            connection_id,
            confluence_config.passage_hash,
            confluence_config.page_path,
        )
    return "Source text fetching not implemented"
