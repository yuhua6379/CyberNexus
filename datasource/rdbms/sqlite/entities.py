from sqlalchemy import Column, String, Integer, Enum, UniqueConstraint
from datasource.rdbms.base import OrmBaseModel
from datasource.rdbms.sqlite.engine import Base


class ChatLogModel(OrmBaseModel, Base):
    # 用于记录
    __tablename__ = 'vb_chatlog'

    character1_id = Column(Integer, nullable=True)
    character2_id = Column(Integer, nullable=True)
    character1_message = Column(String(10000), nullable=True)
    character2_message = Column(String(10000), nullable=True)
    version = Column(String(32), nullable=True)


class HistoryModel(OrmBaseModel, Base):
    __tablename__ = "vb_history"
    character1_id = Column(Integer, nullable=True)
    character2_id = Column(Integer, nullable=True)
    character1_message = Column(String(10000), nullable=True)
    character2_message = Column(String(10000), nullable=True)


class CharacterModel(OrmBaseModel, Base):
    __tablename__ = "vb_character"
    name = Column(String(100), nullable=True, unique=True)
    type = Column(Enum("bot", "user"), nullable=True)

# class Bill
