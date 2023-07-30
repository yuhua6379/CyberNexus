from sqlalchemy.orm import sessionmaker

from .tables import *
from .engine import engine

sqlite_session = None


def initialize():
    global sqlite_session
    if sqlite_session is None:
        Base.metadata.create_all(engine, checkfirst=True)
        sqlite_session = sessionmaker(bind=engine)()


def get_session():
    initialize()
    return sqlite_session
