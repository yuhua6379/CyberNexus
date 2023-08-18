from typing import List

from common.base_thread import get_logger
from model.llm_broker import LLMBrokerBuilder
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History


class ConcludeAbility:
    """总结能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_broker_builder: LLMBrokerBuilder, target_character: Character, broker: PromptBroker):
        self.llm_broker_builder = llm_broker_builder
        self.target_character = target_character
        self.broker = broker

    def rank(self, memory: str):
        session = self.broker.rank_prompt(memory)
        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.broker.factory.get_name_of_system())
        llm_broker = self.llm_broker_builder.build(character1=god,
                                                   character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        session = llm_broker.chat(session)

        get_logger().info(f"rank return: {session}")
        return session.get_context()

    def impress(self, history_list: List[History], other_character: Character, impression_before: str):
        session = self.broker.impress_prompt(self.target_character, other_character, history_list, impression_before)
        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.broker.factory.get_name_of_system())
        llm_broker = self.llm_broker_builder.build(character1=god,
                                                   character2=self.target_character)

        # 把总结的history形成impress放到long term memory里面
        context = llm_broker.chat(session).get_context()

        get_logger().info(f"impress return: {context}")
        return context

    def conclude(self, history_list: List[History], other_character: Character):
        session = self.broker.conclude_prompt(self.target_character, other_character, history_list)
        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.broker.factory.get_name_of_system())
        llm_broker = self.llm_broker_builder.build(character1=god,
                                                   character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        context = llm_broker.chat(session).get_context()

        get_logger().info(f"conclusion return: {context}")
        return context
