import logging
from typing import List

from bot.agent import AgentBuilder
from bot.config.base_conf import CONCLUDE_PROMPT_TEMPLATE, NANE_OF_SYSTEM, HISTORY_FORMAT
from repo.character import Character
from repo.history import History


class ConcludeAbility:
    """总结能力的具体实现，用上帝模式调用llm"""

    def __init__(self, llm_agent_builder: AgentBuilder, target_character: Character):
        self.llm_agent_builder = llm_agent_builder
        self.target_character = target_character

    def conclude(self, history_list: List[History]):
        history_string = "\n".join([str(history) for history in history_list])
        logging.debug("concluding...\n" + history_string)
        conclude_prompt = CONCLUDE_PROMPT_TEMPLATE.format(history=history_string, history_format=HISTORY_FORMAT)

        # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
        god = Character.get_by_name(NANE_OF_SYSTEM)
        agent = self.llm_agent_builder.build(prompt="",
                                             character1=god,
                                             character2=self.target_character)

        # 把总结的history形成memory放到long term memory里面
        conclusion = agent.chat(conclude_prompt)
        return conclusion
