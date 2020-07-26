from __future__ import annotations
import logging

from mongoengine import connect


_LOGGER = logging.getLogger(__name__)


def configure_connection(config):
    connect(
        host=f"mongodb+srv://{config['mongodb']['username']}:{config['mongodb']['password']}@{config['mongodb']['host']}"
    )
