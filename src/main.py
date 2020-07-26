from __future__ import annotations
import click

from src.manager import mock_events
from src.manager import mongo
from src.manager import poll_events
from src.manager import sql


@click.group()
def cli() -> None:
    pass


def main() -> None:
    [
        cli.add_command(command)
        for command in [
            mock_events.mock_events,
            mongo.mongo_insert,
            poll_events.poll_events,
            sql.sql_create_table,
            sql.sql_drop_table,
            sql.sql_insert,
        ]
    ]
    cli()


if __name__ == "__main__":
    main()
