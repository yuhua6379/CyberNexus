from model.entities.message import Message
from repo.character import Character
from repo.history import History, Direction


class ShortTermMemory:
    def __init__(self, character: Character, max_length: int):
        self.character = character
        self.max_length = max_length

    def add(self, history: History):
        History.add(history)

    def shrink(self, shrink_all=False):
        history_list = History.get_not_remembered_history_by_character_id(self.character.id)

        if shrink_all is True:
            # 全部shrink掉
            return history_list

        if len(history_list) >= self.max_length:
            shrink_cnt = int(len(history_list) / 2)
            ret_list = history_list[0: shrink_cnt]

            return ret_list
        return []

    @classmethod
    def batch_set_history_remembered(cls, ids: list[int]):
        History.batch_set_history_remembered(ids)

    @classmethod
    def batch_set_history_impressed(cls, ids: list[int]):
        History.batch_set_history_impressed(ids)

    def get_history(self) -> list[History]:
        return History.get_not_remembered_history_by_character_id(self.character.id)

    def get_history_with_character(self, other_character: Character) -> list[History]:
        return History.get_not_remembered_history_by_couple_character_id(self.character.id, other_character.id)

    def get_not_impressed_history_with_character(self, other_character: Character) -> list[History]:
        return History.get_not_impressed_history_by_couple_character_id(self.character.id, other_character.id)
