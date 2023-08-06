import logging
from typing import List

from pydantic import BaseModel

from bot.agent import AgentBuilder
from bot.brain.shorterm_memory import ShortTermMemory
from bot.config.base_conf import SHORT_TERM_PLAN_PROMPT_TEMPLATE, NANE_OF_SYSTEM, HISTORY_TEMPLATE, \
    LONG_TERM_PLAN_PROMPT_TEMPLATE
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
                 st_memory: ShortTermMemory):
        self.llm_agent_builder = llm_agent_builder
        self.target_character = target_character
        self.factory = factory
        self.st_memory = st_memory

    def short_term_ability(self, latest_long_term_plan: Plan):
        plan_guide = SHORT_TERM_PLAN_PROMPT_TEMPLATE.format(history=self.st_memory.to_prompt(),
                                                            long_term_plan=latest_long_term_plan)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{self.factory.build()}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        plan = agent.chat(plan_guide)

        return Plan(plan=[plan])

    def long_term_ability(self, steps_of_plan: int):
        plan_guide = LONG_TERM_PLAN_PROMPT_TEMPLATE.format(history=self.st_memory.to_prompt(),
                                                           steps_of_round=steps_of_plan)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        prompt = f'{self.factory.build()}\n\n'  # 基础人物设定
        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=god,
                                             character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        plan = agent.chat(plan_guide)
        return Plan.parse_raw(plan)
