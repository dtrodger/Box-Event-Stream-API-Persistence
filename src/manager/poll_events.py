import logging
import time

import click

from src import utils
from src import box_utils
from src.sql import utils as sql_utils
from src.sql.models.box_event import BoxEventSQLManager


_LOGGER = logging.getLogger(__name__)


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def poll_events(env, config):
    sql_utils.configure_connection(config)
    box_event_sql = BoxEventSQLManager(sql_utils.connection)
    box_client = box_utils.configure_box_client(config)
    created_after = config["box"]["event_stream_created_after"]
    try:
        while True:
            events = box_client.events().get_admin_events(created_after=created_after)
            length = len(events['entries'])
            if length > 1:
                for event in events['entries']:
                    box_event_sql.insert_box_event_from_dict(event.response_object)
                else:
                    created_after = event.response_object["created_at"]
            else:
                time.sleep(60 * 10)
    except Exception as e:
        _LOGGER.error(e)
        config["box"]["event_stream_created_after"] = created_after
        utils.write_configuration(env, config)
