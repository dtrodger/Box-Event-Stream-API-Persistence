import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


log = logging.getLogger(__name__)


def configure_connection(config):
    global connection
    connection = create_engine(
        f"postgres://{config['sql']['username']}:{config['sql']['password']}@{config['sql']['host']}:{config['sql']['port']}/{config['sql']['database']}"
    )


base = declarative_base()
connection = None
