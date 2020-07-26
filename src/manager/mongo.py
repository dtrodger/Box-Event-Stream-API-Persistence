import logging

import click

from src import utils
from src.mongo import utils as mongo_utils
from src.mongo.models.box_event import BoxEvent


_LOGGER = logging.getLogger(__name__)


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def mongo_insert(env, config):
    mongo_utils.configure_connection(config)
    event = utils.load_mock_event()
    BoxEvent.insert_box_event_from_dict(event)
