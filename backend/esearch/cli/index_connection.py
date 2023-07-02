import click

from esearch.core.connection import ConnectionEntity
from esearch.core.index_connection import index_connection
from esearch.core.models.embeddings.e5 import E5Basev2


@click.command("ingest_connection")
@click.option(
    "--domain",
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
def ingest_connection_command(domain: str, email: str, token: str) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli ingest_connection \
            --domain "https://bpc-ai.atlassian.net" \
            --email "maximeduvalsy@gmail.com" \
            --token ""
    """
    connection = ConnectionEntity(
        atlassian_email=email,
        atlassian_token=token,
        domain=domain,
        name="From_CLI",
        status="Creating",
        user_id="yyyy",
        id="xxxx",
        created_at="2021-01-01",
    )
    embedder = E5Basev2()
    return index_connection(connection, embedder)
