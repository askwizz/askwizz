import click
from esearch.cli.index_confluence import ingest_confluence_command

_cli = click.Group(
    commands=[
        ingest_confluence_command,
    ],
)

_cli()
