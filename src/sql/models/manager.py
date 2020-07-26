from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import sessionmaker, scoped_session


class SQLManager(metaclass=ABCMeta):
    def __init__(self, connection):
        self.session = self.thread_safe_session(connection)

    @property
    @abstractmethod
    def table(self):
        pass

    @staticmethod
    def thread_safe_session(connection):
        session_factory = sessionmaker(bind=connection)
        Session = scoped_session(session_factory)

        return Session()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, obj):
        self.session.add(obj)
        self.commit()

    def get(self, **kwargs):
        return self.get_all(**kwargs).first()

    def get_all(self, **kwargs):
        return self.session.query(self.table).filter_by(**kwargs)

    def get_all_order_by(self, order_by, **kwargs):
        return self.session.query(self.table).filter_by(**kwargs).order_by(order_by)

    def exists(self, **kwargs):
        return self.get(**kwargs) is not None

    def delete(self, q_record):
        self.session.delete(q_record)
        self.commit()

    def delete_all(self, **kwargs):
        q_records = self.get_all(**kwargs)
        for q_record in q_records:
            self.delete(q_record)
