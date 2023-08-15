from sqlalchemy import Column, String, Integer, Enum, Boolean

from datasource.rdbms.base_entities import OrmBaseModel, Base
from datasource.rdbms.sql import Json


class ChatLogModel(OrmBaseModel, Base):
    # 用于记录
    __tablename__ = 'vb_chatlog'

    character1_id = Column(Integer, nullable=False)
    character2_id = Column(Integer, nullable=False)
    character1_message = Column(String(10000), nullable=False)
    character2_message = Column(String(10000), nullable=False)
    version = Column(String(32), nullable=False)


class HistoryModel(OrmBaseModel, Base):
    __tablename__ = "vb_history"
    main_character_id = Column(Integer, nullable=False, index=True)
    other_character_id = Column(Integer, nullable=False, index=True)

    main_message = Column(String(10000), nullable=False, default="")
    other_message = Column(String(10000), nullable=False, default="")

    main_action = Column(String(10000), nullable=False, default="")
    other_action = Column(String(10000), nullable=False, default="")

    main_stop = Column(Integer, nullable=False)
    other_stop = Column(Integer, nullable=False)

    direction = Column(Enum("to_other", "to_main"), nullable=False)

    remembered = Column(Boolean, default=False, nullable=False)
    impressed = Column(Boolean, default=False, nullable=False)


class CharacterModel(OrmBaseModel, Base):
    __tablename__ = "vb_character"
    name = Column(String(100), nullable=False, unique=True)
    type = Column(Enum("bot", "user", "system"), nullable=False)
    character_prompt = Column(String(10000), nullable=True, unique=False, default="")
    character_appearance = Column(String(10000), nullable=True, unique=False, default="")


class MemoryModel(OrmBaseModel, Base):
    __tablename__ = "vb_memory"
    character_id = Column(Integer, nullable=False)
    vector_db_id = Column(String(64), nullable=False, unique=True)
    content = Column(String(60000), nullable=False)


class ScheduleModel(OrmBaseModel, Base):
    __tablename__ = 'vb_schedule'
    character_id = Column(Integer, nullable=False, unique=True)
    items_to_do = Column(Json, nullable=False, default='[]')
    item_doing = Column(String(1000), nullable=True)


class ScheduleLogModel(OrmBaseModel, Base):
    __tablename__ = 'vb_schedule_log'
    character_id = Column(Integer, nullable=False, index=True)
    item_done = Column(String(1000), nullable=False)


class ImpressionModel(OrmBaseModel, Base):
    __tablename__ = "vb_impression"
    main_character_id = Column(Integer, nullable=False, index=True)
    other_character_id = Column(Integer, nullable=False, index=True)
    impression = Column(String(1000), nullable=False)
