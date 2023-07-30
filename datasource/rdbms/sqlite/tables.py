from sqlalchemy import Column, String
from datasource.rdbms.base import OrmBaseModel
from datasource.rdbms.sqlite.engine import Base


class ChatLog(OrmBaseModel, Base):
    __tablename__ = 'vb_chatlog'

    user = Column(String(10000))
    bot = Column(String(10000))
    version = Column(String(32))
