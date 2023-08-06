from sqlalchemy import Column, String, Integer, Enum, Boolean

from bot.config.base_conf import EMPTY_ACTION, EMPTY_MESSAGE
from datasource.rdbms.base_entities import OrmBaseModel, Base


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

    main_message = Column(String(10000), nullable=False, default=EMPTY_ACTION)
    other_message = Column(String(10000), nullable=False, default=EMPTY_MESSAGE)

    main_action = Column(String(10000), nullable=False, default=EMPTY_ACTION)
    other_action = Column(String(10000), nullable=False, default=EMPTY_MESSAGE)

    direction = Column(Enum("to_other", "to_main"), nullable=False)

    remembered = Column(Boolean, default=False, nullable=False)


class CharacterModel(OrmBaseModel, Base):
    __tablename__ = "vb_character"
    name = Column(String(100), nullable=False, unique=True)
    type = Column(Enum("bot", "user", "system"), nullable=False)
    character_prompt = Column(String(10000), nullable=True, unique=False, default="")


class MemoryModel(OrmBaseModel, Base):
    __tablename__ = "vb_memory"
    character_id = Column(Integer, nullable=False)
    vector_db_id = Column(String(64), nullable=False, unique=True)
    content = Column(String(60000), nullable=False)
