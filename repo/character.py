from enum import Enum
from typing import Optional

from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel
from prompt.prompt_factory.virtual_character import VirtualCharacter


class Character(BaseModel, orm_mode=True):
    """
    角色entity,主要用于在bot内部传递数据
    """

    class CharacterType(Enum):
        bot = "bot"
        user = "user"
        system = "system"

    id: int
    name: str
    type: CharacterType
    character_prompt: str

    @classmethod
    def get_by_name(cls, name: str):
        with rdbms_instance.get_session() as session:
            result = session.query(CharacterModel).filter(CharacterModel.name == name).one()
            return Character.from_orm(result)

    @classmethod
    def get(cls, id_: int):
        with rdbms_instance.get_session() as session:
            result = session.query(CharacterModel).get(id_)
            return cls.from_orm(result)
