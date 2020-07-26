import click

from src import utils
from src.sql.models.box_event import BoxEvent, BoxEventSQLManager
from src.sql import utils as sql_utils


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def sql_create_table(env, config):
    sql_utils.configure_connection(config)
    sql_utils.base.metadata.create_all(sql_utils.connection)


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def sql_drop_table(env, config):
    sql_utils.configure_connection(config)
    BoxEvent.__table__.drop(sql_utils.connection)


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def sql_insert(env, config):
    sql_utils.configure_connection(config)
    box_event_sql = BoxEventSQLManager(sql_utils.connection)
    event = utils.load_mock_event()
    box_event_sql.insert_box_event_from_dict(event)
