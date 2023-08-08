from bot.message import Message
from datasource.vectordb.entities import Document
from model.base_prompt_factory import BasePromptFactory
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class PromptBroker:
    def __init__(self, factory: BasePromptFactory):
        self.factory = factory

    def stimulus_of_character(self,
                              input_character: Character,
                              history_list: list[History],
                              relative_memory: list[Document],
                              recent_memory: list[Memory]):
        return self.factory.on_build_stimulus_of_character(
            input_character,
            history_list,
            relative_memory,
            recent_memory)

    def conclude_prompt(self, history_list: list[History]):
        return self.factory.on_build_conclude_prompt(history_list)

    def schedule_prompt(self, character: Character,
                        item_done: list[str],
                        steps: int,
                        recent_memory: list[Memory]):
        return self.factory.on_build_schedule_prompt(character,
                                                     item_done,
                                                     steps,
                                                     recent_memory)

    def determine_whether_item_finish_prompt(self,
                                             character: Character,
                                             target_item: str,
                                             history_list: list[History],
                                             recent_memory: list[Memory]):
        return self.factory.on_build_determine_whether_item_finish_prompt(
            character, target_item, history_list, recent_memory)

    def react_prompt(self,
                     character: Character,
                     input_: Message,
                     item_doing: str,
                     history_list: list[History],
                     relative_memory: list[Document],
                     recent_memory: list[Memory]):
        return self.factory.on_build_react_prompt(
            character, input_, item_doing, history_list, relative_memory, recent_memory)
