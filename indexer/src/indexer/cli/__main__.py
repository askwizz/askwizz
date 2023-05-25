import click

from indexer.cli.commands.ingest import ingest_command
from indexer.cli.commands.search import search_command

_cli = click.Group(
    commands=[
        ingest_command,
        search_command,
    ],
)

_cli()
