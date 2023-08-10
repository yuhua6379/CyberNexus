from model.entities.message import Message
from datasource.vectordb.entities import Response
from model.base_prompt_factory import BasePromptFactory
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class PromptBroker:
    def __init__(self, factory: BasePromptFactory):
        self.factory = factory

    def stimulus_of_character(self,
                              main_character: Character,
                              other_character: Character,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]):
        return self.factory.on_build_stimulus_of_character(
            main_character,
            other_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

    def conclude_prompt(self, main_character: Character, history_list: list[History]):
        return self.factory.on_build_conclude_prompt(main_character, history_list)

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
