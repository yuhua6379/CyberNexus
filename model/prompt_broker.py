from datasource.vectordb.entities import Response
from model.base_prompt_factory import BasePromptFactory
from model.entities.message import Message
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class PromptBroker:
    def __init__(self, factory: BasePromptFactory):
        self.factory = factory

    def set_debug_prompt(self, debug_prompt: str):
        self.factory.set_debug_prompt(debug_prompt)

    def do_something_prompt(self, main_character: Character, do_something: str):
        ret = self.factory.on_build_do_something_prompt(main_character, do_something)
        return ret

    def provoked_by_character_prompt(self,
                                     main_character: Character,
                                     other_character: Character,
                                     item_doing: str,
                                     history_list: list[History],
                                     relative_memory: list[Response],
                                     recent_memory: list[Memory]):
        return self.factory.on_build_provoked_by_character(
            main_character,
            other_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

    def conclude_prompt(self, main_character: Character, other_character: Character, history_list: list[History]):
        return self.factory.on_build_conclude_prompt(main_character, other_character, history_list)

    def impress_prompt(self, main_character: Character, other_character: Character, history_list: list[History],
                       impression_before: str):
        return self.factory.on_build_impress_prompt(main_character, other_character, history_list, impression_before)

    def rank_prompt(self, memory: str):
        return self.factory.on_build_rank_prompt(memory)

    def schedule_prompt(self, main_character: Character,
                        item_done: list[str],
                        steps: int,
                        recent_memory: list[Memory]):
        return self.factory.on_build_schedule_prompt(main_character,
                                                     item_done,
                                                     steps,
                                                     recent_memory)

    def determine_whether_item_finish_prompt(self,
                                             main_character: Character,
                                             target_item: str,
                                             history_list: list[History],
                                             recent_memory: list[Memory]):
        return self.factory.on_build_determine_whether_item_finish_prompt(
            main_character, target_item, history_list, recent_memory)

    def react_prompt(self,
                     main_character: Character,
                     other_character: Character,
                     input_: Message,
                     item_doing: str,
                     history_list: list[History],
                     relative_memory: list[Response],
                     recent_memory: list[Memory]):
        return self.factory.on_build_react_prompt(
            main_character, other_character,
            input_, item_doing, history_list, relative_memory, recent_memory)
