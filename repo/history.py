from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import and_

from bot.config.base_conf import EMPTY_ACTION, EMPTY_MESSAGE
from bot.message import Message
from datasource.config import rdbms_instance
from datasource.rdbms.entities import HistoryModel
from repo.character import Character


class Direction(Enum):
    to_other = "to_other"
    to_main = "to_main"


class History(BaseModel):
    id: Optional[int]
    main_character: Character
    other_character: Character
    main_message: Optional[str] = EMPTY_MESSAGE
    other_message: Optional[str] = EMPTY_MESSAGE
    main_action: Optional[str] = EMPTY_ACTION
    other_action: Optional[str] = EMPTY_ACTION

    direction: Direction

    def __str__(self):

        history_str = ""
        if self.direction == Direction.to_other:
            history_str += str(Message(from_character=self.main_character.name,
                                       to_character=self.other_character.name,
                                       action=self.main_action,
                                       message=self.main_message)) + '\n\n'

        else:
            history_str += str(Message(from_character=self.other_character.name,
                                       to_character=self.main_character.name,
                                       action=self.other_action,
                                       message=self.other_message)) + '\n\n'

        return history_str

    @classmethod
    def from_model(cls, model: HistoryModel):

        return cls(id=model.id,
                   main_character=Character.get(model.main_character_id),
                   other_character=Character.get(model.other_character_id),
                   main_message=model.main_message,
                   other_message=model.other_message,
                   main_action=model.main_action,
                   other_action=model.other_action,
                   direction=model.direction
                   )

    @classmethod
    def add(cls, history):
        history: cls
        model = HistoryModel()
        model.main_character_id = history.main_character.id
        model.other_character_id = history.other_character.id
        model.main_message = history.main_message
        model.other_message = history.other_message
        model.main_action = history.main_action
        model.other_action = history.other_action

        model.direction = history.direction.value

        with rdbms_instance.get_session() as session:
            session.add(model)
            session.commit()

    @classmethod
    def get_available_history_by_character_id(cls, character_id: int):
        with rdbms_instance.get_session() as session:
            results = session.query(HistoryModel).filter(
                and_(
                    HistoryModel.remembered == False,
                    HistoryModel.main_character_id == character_id)).all()
            return [cls.from_model(model) for model in results]

    @classmethod
    def batch_set_history_remembered(cls, ids: list[int]):
        with rdbms_instance.get_session() as session:
            ret = session.query(HistoryModel).filter(HistoryModel.id.in_(ids)).update({HistoryModel.remembered: True})
            session.commit()
