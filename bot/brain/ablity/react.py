from bot.agent import AgentBuilder
from bot.message import Message
from common.base_thread import get_logger
from datasource.vectordb.entities import Document
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

    def stimulus_of_character(self,
                              input_character: Character,
                              history_list: list[History],
                              relative_memory: list[Document],
                              recent_memory: list[Memory]):
        prompt = self.prompt_broker.stimulus_of_character(
            self.character,
            input_character,
            history_list,
            relative_memory,
            recent_memory)

        agent = self.llm_agent_builder.build(prompt="",
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(prompt)

        get_logger().info(f'stimulus_of_character return:{ret}\n')

        message = Message.parse_raw(ret)

        return message

    def react(self,
              input_: Message,
              input_character: Character,
              item_doing: str,
              history_list: list[History],
              relative_memory: list[Document],
              recent_memory: list[Memory]):
        prompt = self.prompt_broker.react_prompt(
            self.character,
            input_character,
            input_,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

        agent = self.llm_agent_builder.build(prompt="",
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(prompt)

        get_logger().info(f'react return:{ret}\n')

        message = Message.parse_raw(ret)

        return message
