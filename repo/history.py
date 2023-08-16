from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import and_, or_

from datasource.config import rdbms_instance
from datasource.rdbms.entities import HistoryModel
from model.entities.message import Message
from repo.character import Character


class Direction(Enum):
    to_other = "to_other"
    to_main = "to_main"


class History(BaseModel):
    id: Optional[int]
    main_character: Character
    other_character: Character
    main_message: Optional[str] = ""
    other_message: Optional[str] = ""
    main_action: Optional[str] = ""
    other_action: Optional[str] = ""

    main_stop: int
    other_stop: int

    direction: Direction

    def to_prompt(self, simple_string=False):

        history_str = ""
        if self.direction == Direction.to_other:
            history_str += Message(from_character=self.main_character.name,
                                   to_character=self.other_character.name,
                                   action=self.main_action,
                                   message=self.main_message,
                                   stop=self.main_stop).to_prompt(simple_string) + '\n\n'

            history_str += Message(from_character=self.other_character.name,
                                   to_character=self.main_character.name,
                                   action=self.other_action,
                                   message=self.other_message,
                                   stop=self.other_stop).to_prompt(simple_string) + '\n\n'

        if self.direction == Direction.to_main:
            history_str += Message(from_character=self.other_character.name,
                                   to_character=self.main_character.name,
                                   action=self.other_action,
                                   message=self.other_message,
                                   stop=self.other_stop).to_prompt(simple_string) + '\n\n'

            history_str += Message(from_character=self.main_character.name,
                                   to_character=self.other_character.name,
                                   action=self.main_action,
                                   message=self.main_message,
                                   stop=self.main_stop).to_prompt(simple_string) + '\n\n'

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
                   direction=model.direction,
                   main_stop=model.main_stop,
                   other_stop=model.other_stop
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
        model.main_stop = history.main_stop
        model.other_stop = history.other_stop

        model.direction = history.direction.value

        with rdbms_instance.get_session() as session:
            session.add(model)
            session.commit()

    @classmethod
    def get_not_remembered_history_by_character_id(cls, character_id: int):
        with rdbms_instance.get_session() as session:
            filter_ = session.query(HistoryModel).filter(HistoryModel.remembered == False)
            filter_ = filter_.filter(HistoryModel.main_character_id == character_id)

            results = filter_.all()
            return [cls.from_model(model) for model in results]

    @classmethod
    def get_not_remembered_history_by_couple_character_id(cls, main_character_id: int, other_character_id: int):
        with rdbms_instance.get_session() as session:
            filter_ = session.query(HistoryModel).filter(HistoryModel.remembered == False)
            filter_ = filter_.filter(HistoryModel.main_character_id == main_character_id)
            filter_ = filter_.filter(HistoryModel.other_character_id == other_character_id)
            results = filter_.all()
            return [cls.from_model(model) for model in results]

    @classmethod
    def batch_set_history_remembered(cls, ids: list[int]):
        with rdbms_instance.get_session() as session:
            ret = session.query(HistoryModel).filter(HistoryModel.id.in_(ids)).update({HistoryModel.remembered: True})
            session.commit()

    @classmethod
    def get_not_impressed_history_by_couple_character_id(cls, main_character_id: int, other_character_id: int):
        with rdbms_instance.get_session() as session:
            filter_ = session.query(HistoryModel).filter(HistoryModel.impressed == False)
            filter_ = filter_.filter(HistoryModel.main_character_id == main_character_id)
            filter_ = filter_.filter(HistoryModel.other_character_id == other_character_id)
            results = filter_.all()
            return [cls.from_model(model) for model in results]

    @classmethod
    def batch_set_history_impressed(cls, ids: list[int]):
        with rdbms_instance.get_session() as session:
            ret = session.query(HistoryModel).filter(HistoryModel.id.in_(ids)).update({HistoryModel.impressed: True})
            session.commit()
