from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datasource.rdbms.base import RDBMSBase, Rdbms
from datasource.rdbms.entities import *

_engine = None
_session_maker: Optional[sessionmaker] = None


class Sqlite(RDBMSBase):

    def __init__(self, conf: Rdbms):

        super().__init__(conf)

    @contextmanager
    def get_session(self):
        self.initialize()
        session = _session_maker()
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

    def initialize(self):
        global _engine
        global _session_maker
        if _engine is None:
            _engine = create_engine(self.conf.uri, pool_size=self.conf.pool_size)
            Base.metadata.create_all(_engine, checkfirst=True)
            _session_maker = sessionmaker(bind=_engine)
