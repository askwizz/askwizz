import atexit
import cProfile
import datetime
import io
import pstats
from datetime import timezone
from typing import Any, Callable

import click

from esearch.core.connection.definition import (
    AtlassianData,
    ConnectionConfiguration,
    ConnectionSource,
    ConnectionStatus,
)
from esearch.core.connection.entity import Connection
from esearch.core.connection.index import index_connection
from esearch.core.models.embeddings.e5 import E5v2
from esearch.db.engine import get_db
from esearch.services.milvus.client import Milvus


def profile_command(
    profiled_function: Callable[[], None], *args: Any, **kwargs: Any  # noqa: ANN401
) -> None:
    print("Profiling...")
    pr = cProfile.Profile()
    pr.enable()

    profiled_function(*args, **kwargs)

    def exit_profile() -> None:
        pr.disable()
        pr.dump_stats("index.prof")
        print("Profiling completed")
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats()
        print(s.getvalue())

    atexit.register(exit_profile)


def ingest_connection(
    atlassian_domain: str, email: str, token: str, sql_url: str
) -> None:
    user_id = "yyyy"
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
        user_id=user_id,
        id_="xxxx",
        created_at=datetime.datetime.now(timezone.utc),
        indexed_at=datetime.datetime.now(timezone.utc),
        source=ConnectionSource.CONFLUENCE,
        connection_key="xxxx",
    )
    embedder = E5v2()
    db_generator = get_db(sql_url)()
    db = next(db_generator)
    index_connection(
        connection, embedder, db, milvus_client=Milvus(user_id, embedder=embedder)
    )


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
@click.option("--profile", is_flag=True)
def ingest_connection_command(
    atlassian_domain: str, email: str, token: str, sql_url: str, profile: bool
) -> None:
    """Ingest confluence space into a database.
    poetry run python -m esearch.cli ingest_connection \
            --atlassian_domain "bpc-ai.atlassian.net" \
            --email "maximeduvalsy@gmail.com" \
            --token "" \
            --sql_url "postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
    """
    if profile:
        profile_command(ingest_connection, atlassian_domain, email, token, sql_url)  # type: ignore  # noqa: E501
    else:
        ingest_connection(atlassian_domain, email, token, sql_url)
