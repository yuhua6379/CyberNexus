from typing import List

from model.agent import AgentBuilder
from common.base_thread import get_logger
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History


class ConcludeAbility:
    """总结能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_agent_builder: AgentBuilder, target_character: Character, broker: PromptBroker):
        self.llm_agent_builder = llm_agent_builder
        self.target_character = target_character
        self.broker = broker

    def rank(self, memory: str):
        session = self.broker.rank_prompt(memory)
        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.broker.factory.get_name_of_system())
        agent = self.llm_agent_builder.build(character1=god,
                                             character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        session = agent.chat(session)

        get_logger().info(f"rank return: {session}")
        return session.get_result()

    def conclude(self, history_list: List[History], other_character: Character):
        session = self.broker.conclude_prompt(self.target_character, other_character, history_list)
        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.broker.factory.get_name_of_system())
        agent = self.llm_agent_builder.build(character1=god,
                                             character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        session = agent.chat(session)

        get_logger().info(f"conclusion return: {session}")
        return session.get_result()
