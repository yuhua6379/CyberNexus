from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from .entities import *
from .engine import engine

sqlite_session = None


def initialize():
    global sqlite_session
    if sqlite_session is None:
        Base.metadata.create_all(engine, checkfirst=True)
        sqlite_session = sessionmaker(bind=engine)()


@contextmanager
def get_session():
    initialize()
    try:
        yield sqlite_session
    except:
        sqlite_session.rollback()
        raise
    else:
        sqlite_session.commit()
