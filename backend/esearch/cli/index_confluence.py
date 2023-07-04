import datetime

import click

from esearch.core.connection.definition import (
    AtlassianData,
    ConnectionConfiguration,
    ConnectionSource,
    ConnectionStatus,
)
from esearch.core.connection.entity import Connection
from esearch.core.connection.index import index_connection
from esearch.core.models.embeddings.e5 import E5Basev2
from esearch.db.engine import get_db


@click.command("ingest_connection")
@click.option(
    "--atlassian_domain",
    type=str,
    required=True,
)
@click.option(
    "--email",
    type=str,
    required=True,
)
@click.option(
    "--token",
    type=str,
    required=True,
)
@click.option(
    "--sql_url",
    type=str,
    required=True,
)
def ingest_connection_command(
    atlassian_domain: str, email: str, token: str, sql_url: str
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli ingest_connection \
            --atlassian_domain "https://bpc-ai.atlassian.net" \
            --email "maximeduvalsy@gmail.com" \
            --token "" \
            --sql_url "postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
    """
    connection = Connection(
        configuration=ConnectionConfiguration(
            atlassian=AtlassianData(
                atlassian_email=email,
                atlassian_token=token,
                atlassian_domain=atlassian_domain,
            )
        ),
        name="From_CLI",
        status=ConnectionStatus.ACTIVE,
        user_id="yyyy",
        id_="xxxx",
        created_at=datetime.datetime.now(),
        indexed_at=datetime.datetime.now(),
        source=ConnectionSource.CONFLUENCE,
    )
    embedder = E5Basev2()
    db = get_db(sql_url)()
    index_connection(connection, embedder, db)
