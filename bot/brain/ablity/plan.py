import logging
from typing import List

from pydantic import BaseModel

from bot.agent import AgentBuilder
from bot.brain.longterm_memory import LongTermMemory
from bot.brain.shorterm_memory import ShortTermMemory
from bot.config.base_conf import SHORT_TERM_PLAN_PROMPT_TEMPLATE, NANE_OF_SYSTEM, HISTORY_TEMPLATE, \
    LONG_TERM_PLAN_PROMPT_TEMPLATE, HISTORY_FORMAT, PLAN_FORMAT
from common.base_thread import get_logger
from prompt.prompt_factory.core import PromptFactory
from repo.character import Character


class Plan(BaseModel):
    plan: list[str]

    def to_prompt(self):
        ret = ""
        for idx, step in enumerate(self.plan):
            ret += f"{idx + 1}.{step}"
        if len(ret) == 0:
            ret = "没有长期计划"
        return ret


class PlanAbility:
    """规划能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_agent_builder: AgentBuilder,
                 target_character: Character,
                 factory: PromptFactory,
                 st_memory: ShortTermMemory,
                 lt_memory: LongTermMemory):
        self.llm_agent_builder = llm_agent_builder
        self.target_character = target_character
        self.factory = factory
        self.st_memory = st_memory
        self.lt_memory = lt_memory

        self.plan_done = []

    def short_term_ability(self, latest_long_term_plan: Plan):
        plan_guide = SHORT_TERM_PLAN_PROMPT_TEMPLATE.format(memory=self.lt_memory.latest_memory(),
                                                            executed_plan=self.plan_done,
                                                            plan_format=PLAN_FORMAT,
                                                            long_term_plan=latest_long_term_plan)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{self.factory.build()}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=self.target_character)

        get_logger().debug(f"short_plan prompt: \n{prompt}")
        get_logger().debug(f"short_plan guide: \n{plan_guide}")

        # 把总结的history形成memory放到long term memory里面
        plan = agent.chat(plan_guide)

        get_logger().info(f"short_plan return: \n{plan}")

        plan = Plan.parse_raw(plan)

        self.plan_done.append(plan)

        return plan

    def long_term_ability(self, steps_of_plan: int):
        plan_guide = LONG_TERM_PLAN_PROMPT_TEMPLATE.format(memory=self.lt_memory.latest_memory(),
                                                           plan_format=PLAN_FORMAT, steps_of_round=steps_of_plan)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{self.factory.build()}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=self.target_character)

        get_logger().debug(f"long_plan prompt: \n{prompt}")
        get_logger().debug(f"long_plan guide: \n{plan_guide}")
        # 把总结的history形成memory放到long term memory里面
        plan = agent.chat(plan_guide)

        get_logger().info(f"long_plan return: \n{plan}")
        plan = Plan.parse_raw(plan)
        return plan
