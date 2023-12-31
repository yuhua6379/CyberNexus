from common.base_thread import get_logger
from model.llm_broker import LLMBrokerBuilder
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class ScheduleAbility:
    """规划能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_broker_builder: LLMBrokerBuilder,
                 target_character: Character,
                 prompt_broker: PromptBroker):
        self.llm_broker_builder = llm_broker_builder
        self.target_character = target_character
        self.prompt_broker = prompt_broker

    def determine_whether_item_finish(self, target_item: str, history_list: list[History], recent_memory: list[Memory]):
        """输入内容 = 基础人物设定 + 最近的memory + 最近的交互 + 可能正在做的事情"""

        session = self.prompt_broker.determine_whether_item_finish_prompt(self.target_character, target_item,
                                                                          history_list,
                                                                          recent_memory)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.prompt_broker.factory.get_name_of_system())

        llm_broker = self.llm_broker_builder.build(character1=god,
                                                   character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        context = llm_broker.chat(session).get_context()

        get_logger().info(f"really_done_item return: \n{context}")

        return context

    def schedule(self, item_done: list[str], steps: int, recent_memory: list[Memory]):
        """输入内容 = 基础人物设定 + 最近的memory + 多少个step + 完成了的item"""

        session = self.prompt_broker.schedule_prompt(
            self.target_character, item_done, steps, recent_memory)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(self.prompt_broker.factory.get_name_of_system())

        llm_broker = self.llm_broker_builder.build(character1=god,
                                                   character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        context = llm_broker.chat(session).get_context()

        get_logger().info(f"schedule return: \n{context}")
        return context
