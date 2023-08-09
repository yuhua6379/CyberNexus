from bot.message import Message
from repo.character import Character
from repo.history import History, Direction


class ShortTermMemory:
    def __init__(self, character: Character, max_length: int):
        self.character = character
        self.max_length = max_length

    def add(self, character_input: Character, message_in: Message, message_out: Message):
        History.add(History(main_character=self.character,
                            other_character=character_input,
                            main_message=message_out.message,
                            main_action=message_out.action,
                            other_message=message_in.message,
                            other_action=message_in.action,
                            direction=Direction.to_main,
                            main_stop=message_in.stop,
                            other_stop=message_out.stop
                            ))

    def shrink(self, shrink_all=False):
        history_list = History.get_available_history_by_character_id(self.character.id)

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

    def get_history(self) -> list[History]:
        return History.get_available_history_by_character_id(self.character.id)

    def get_history_with_character(self, other_character: Character) -> list[History]:
        return History.get_available_history_by_character_id()
