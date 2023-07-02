import logging

import click

from esearch.cli.index_connection import ingest_connection_command
from esearch.cli.search import search_command

logging.basicConfig(level=logging.DEBUG)

_cli = click.Group(
    commands=[ingest_connection_command, search_command],
)

_cli()
