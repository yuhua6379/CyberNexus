from pydantic import BaseModel

from bot.agent import AgentBuilder
from bot.brain.longterm_memory import LongTermMemory
from bot.brain.shorterm_memory import ShortTermMemory
from bot.config.base_conf import IF_ITEM_DONE_TEMPLATE
from bot.config.base_conf import NANE_OF_SYSTEM, SCHEDULING_PROMPT_TEMPLATE, \
    SCHEDULE_FORMAT
from common.base_thread import get_logger
from repo.character import Character
from repo.history import History


class LLMSchedule(BaseModel):
    schedule: list[str]

    def to_prompt(self):
        ret = ""
        for idx, step in enumerate(self.schedule):
            ret += f"{idx + 1}.{step}"
        if len(ret) == 0:
            ret = ""
        return ret


class ScheduleAbility:
    """规划能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_agent_builder: AgentBuilder,
                 target_character: Character,

                 st_memory: ShortTermMemory,
                 lt_memory: LongTermMemory):
        self.llm_agent_builder = llm_agent_builder
        self.target_character = target_character
        self.st_memory = st_memory
        self.lt_memory = lt_memory

    def really_done_item(self, target_item: str, history_list: list[History]):
        """输入内容 = 基础人物设定 + 最近的memory + 已经执行的plan + 长期的plan"""
        guide = IF_ITEM_DONE_TEMPLATE.format(
            memory=self.lt_memory.latest_memory_to_prompt(),
            item=target_item,
            history_string='\n'.join([history.to_prompt(True) for history in history_list]))

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{self.target_character.character_prompt}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=self.target_character)

        get_logger().debug(f"really_done_item prompt: \n{prompt}")
        get_logger().debug(f"really_done_item guide: \n{guide}")

        # 把总结的history形成memory放到long term memory里面
        item = agent.chat(guide)

        get_logger().info(f"really_done_item return: \n{item}")

        return item

    def schedule(self, character: Character, item_done: list[str], steps: int):
        """输入内容 = 基础人物设定 + 最近的memory + 多少个step"""

        plan_guide = SCHEDULING_PROMPT_TEMPLATE.format(
            memory=self.lt_memory.latest_memory_to_prompt(),  # 最近的memory
            item_done=item_done,  # 已完成的事项
            schedule_format=SCHEDULE_FORMAT, steps=steps)  # 多少个step

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{character.character_prompt}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=character)

        get_logger().debug(f"long_plan prompt: \n{prompt}")
        get_logger().debug(f"long_plan guide: \n{plan_guide}")
        # 把总结的history形成memory放到long term memory里面
        schedule = agent.chat(plan_guide)

        get_logger().info(f"schedule return: \n{schedule}")
        schedule = LLMSchedule.parse_raw(schedule)

        return schedule
