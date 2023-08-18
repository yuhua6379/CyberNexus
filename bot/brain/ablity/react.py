from common.base_thread import get_logger
from datasource.vectordb.entities import Response
from model.entities.message import Message
from model.llm_broker import LLMBrokerBuilder
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class ReactAbility:
    def __init__(self,
                 character: Character,
                 prompt_broker: PromptBroker,
                 llm_broker_builder: LLMBrokerBuilder):
        self.character = character
        self.prompt_broker = prompt_broker
        self.llm_broker_builder = llm_broker_builder

    def provoked_by_character(self,
                              input_character: Character,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]):
        session = self.prompt_broker.provoked_by_character_prompt(
            self.character,
            input_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

        llm_broker = self.llm_broker_builder.build(character1=input_character,
                                                   character2=self.character)
        context = llm_broker.chat(session).get_context()

        get_logger().info(f'provoked_by_character return:{context}\n')

        return context

    def react(self,
              input_: Message,
              input_character: Character,
              item_doing: str,
              history_list: list[History],
              relative_memory: list[Response],
              recent_memory: list[Memory]):
        session = self.prompt_broker.react_prompt(
            self.character,
            input_character,
            input_,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

        llm_broker = self.llm_broker_builder.build(character1=input_character,
                                                   character2=self.character)
        context = llm_broker.chat(session).get_context()

        get_logger().info(f'react return:{context}\n')

        return context
