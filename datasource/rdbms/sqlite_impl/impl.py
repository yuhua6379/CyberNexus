from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datasource.rdbms.base import RDBMSBase, Rdbms
from datasource.rdbms.entities import *


class Sqlite(RDBMSBase):

    def __init__(self, conf: Rdbms):

        super().__init__(conf)
        self.sqlite_session = None

    @contextmanager
    def get_session(self):
        self.initialize()
        try:
            yield self.sqlite_session
        except:
            self.sqlite_session.rollback()
            raise
        else:
            self.sqlite_session.commit()

    def initialize(self):
        if self.sqlite_session is None:
            engine = create_engine(self.conf.uri)
            Base.metadata.create_all(engine, checkfirst=True)
            self.sqlite_session = sessionmaker(bind=engine)()
