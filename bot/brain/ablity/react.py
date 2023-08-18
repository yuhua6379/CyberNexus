from common.base_thread import get_logger
from datasource.vectordb.entities import Response
from model.agent import AgentBuilder
from model.entities.message import Message
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class ReactAbility:
    def __init__(self,
                 character: Character,
                 prompt_broker: PromptBroker,
                 llm_agent_builder: AgentBuilder):
        self.character = character
        self.prompt_broker = prompt_broker
        self.llm_agent_builder = llm_agent_builder

    def provoked_by_character(self,
                              input_character: Character,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]):
        session = self.prompt_broker.provoked_by_character(
            self.character,
            input_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

        agent = self.llm_agent_builder.build(character1=input_character,
                                             character2=self.character)
        session = agent.chat(session)

        get_logger().info(f'provoked_by_character return:{session}\n')

        return session.get_result()

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

        agent = self.llm_agent_builder.build(character1=input_character,
                                             character2=self.character)
        session = agent.chat(session)

        get_logger().info(f'react return:{session}\n')

        return session.get_result()
