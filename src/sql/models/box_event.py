import logging

from sqlalchemy import Column, String, DateTime, Integer

from src.sql import utils
from src.sql.models import manager


_LOGGER = logging.getLogger(__name__)


class BoxEvent(utils.base):
    __tablename__ = "box_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String)
    created_by_email = Column(String)
    created_by_name = Column(String)
    created_at = Column(DateTime)


class BoxEventSQLManager(manager.SQLManager):
    table = BoxEvent

    def __init__(self, engine):
        super().__init__(engine)

    def insert_box_event_from_dict(self, event_dict):
        event = self.table(
            event_type=event_dict["event_type"],
            created_by_email=event_dict["created_by"]["login"],
            created_by_name=event_dict["created_by"]["name"],
            created_at=event_dict["created_at"],
        )

        return event
