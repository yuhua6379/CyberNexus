from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import HistoryModel
from repo.character import Character


class Direction(Enum):
    to_right = "to_right"
    to_left = "to_left"


class History(BaseModel):
    id: Optional[int]
    my_character: Character
    other_character: Character
    my_message: str
    other_message: str

    direction: Direction

    def __str__(self):

        if self.direction == Direction.to_right:
            requester = self.my_character
            req_msg = self.my_message
            responser = self.other_character
            res_msg = self.other_message
        else:
            requester = self.other_character
            req_msg = self.other_message
            responser = self.my_character
            res_msg = self.my_message

        return (f"{requester.name}: {req_msg}\n"
                f"{responser.name}: {res_msg}\n\n")

    @classmethod
    def from_model(cls, model: HistoryModel):

        return cls(id=model.id,
                   my_character=Character.get(model.my_character_id),
                   other_character=Character.get(model.other_character_id),
                   my_message=model.my_message,
                   other_message=model.other_message,
                   direction=model.direction
                   )

    @classmethod
    def add(cls, history):
        history: cls
        model = HistoryModel()
        model.my_character_id = history.my_character.id
        model.other_character_id = history.other_character.id
        model.my_message = history.my_message
        model.other_message = history.other_message
        model.direction = history.direction.value

        with rdbms_instance.get_session() as session:
            session.add(model)
            session.commit()

    @classmethod
    def get_available_history_by_character_id(cls, character_id: int):
        with rdbms_instance.get_session() as session:
            results = session.query(HistoryModel).filter(
                HistoryModel.remembered == False and
                HistoryModel.my_character_id == character_id).all()
            return [cls.from_model(model) for model in results]

    @classmethod
    def batch_set_history_remembered(cls, ids: list[int]):
        with rdbms_instance.get_session() as session:
            ret = session.query(HistoryModel).filter(HistoryModel.id.in_(ids)).update({HistoryModel.remembered: True})
            session.commit()
