import click
from core.index_confluence import index_confluence


@click.command("ingest_confluence")
@click.option(
    "--space",
    type=str,
    required=True,
)
@click.option(
    "--wiki_url",
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
def ingest_confluence_command(
    space: str, wiki_url: str, email: str, token: str
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m indexer.cli ingest_confluence \
            --space "TW" \
            --wiki_url "https://bpc-ai.atlassian.net/wiki" \
            --email "maximeduvalsy@gmail.com" \
            --token ""
    """
    return index_confluence(space, wiki_url, email, token)
