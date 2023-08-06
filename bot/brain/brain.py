from typing import List

from bot.agent import AgentBuilder
from bot.brain.ablity.conclude import ConcludeAbility
from bot.brain.ablity.plan import PlanAbility
from bot.brain.longterm_memory import LongTermMemory
from bot.brain.shorterm_memory import ShortTermMemory
from bot.config.base_conf import MAX_SHORT_TERM_MEMORY, RELATIVE_MEMORY_TEMPLATE, HISTORY_TEMPLATE, \
    REACT_TEMPLATE, HISTORY_FORMAT
from bot.message import Message
from common.base_thread import get_logger
from prompt.prompt_factory.core import PromptFactory
from repo.character import Character
from repo.history import History


class Brain:

    def __init__(self, character: Character, llm_agent_builder: AgentBuilder):
        self.character = character
        self.lt_memory = LongTermMemory(character)
        self.st_memory = ShortTermMemory(max_length=MAX_SHORT_TERM_MEMORY, character=character)
        self.llm_agent_builder = llm_agent_builder
        self.factory = PromptFactory()
        self.factory.append(character.character_prompt)
        self.conclude_ability = ConcludeAbility(self.llm_agent_builder, self.character)

        self.latest_long_term_plan = None
        self.plan_ability = PlanAbility(self.llm_agent_builder, self.character, self.factory, self.st_memory, self.lt_memory)

        self.debug_prompt = ""

    def set_debug_prompt(self, prompt: str):
        self.debug_prompt = prompt.strip()

    def get_debug_prompt(self):
        if len(self.debug_prompt) == 0:
            return ""
        else:
            return self.debug_prompt + "\n\n"

    def associate(self, input_: Message, input_character: Character):
        """机器人大脑对外部刺激联想到某些事情"""
        # 联想的关键词，要包含input_character的名字，否则可能联想不出input_character的记忆
        kw1 = f'{input_character.name}: {input_.message}'
        kw2 = f'{input_character.name}: {input_.action}'
        ret = (f"{self.get_relative_memory_prompt(key_word=kw1)}\n"
               f"{self.get_relative_memory_prompt(key_word=kw2)}").strip()
        if len(ret) == 0:
            return "没有数据"

    def react(self, input_: Message, input_character: Character):
        """
        机器人大脑对外部刺激做出反应:
        1.保证机器人基础设定
        2.从输入associate一些memory
        3.使用llm处理，并作出反应
        4.记录历史到history，必要时转化为memory
        """

        prompt = (f'{self.factory.build()}\n\n'  # 基础人物设定
                  f'{self.get_debug_prompt()}'
                  )
        # c1做出行动，c1对c2说了话，假设llm是c2，等待llm的回应
        react_guide = (f'{HISTORY_FORMAT}\n\n'  # 通用prompt告诉llm用固定格式返回
                       + REACT_TEMPLATE.format(
                    c1=self.character.name,
                    message=f'{HISTORY_TEMPLATE.format(content=self.st_memory.to_prompt())}\n'
                            + str(Message(from_character=input_character.name,
                                    to_character=self.character.name,
                                    action=input_.action,
                                    message=input_.message))))

        # prompt = (f'{self.factory.build()}\n\n'  # 基础人物设定
        #           f'{self.get_debug_prompt()}'
        #           f'{RELATIVE_MEMORY_TEMPLATE.format(content=self.associate(input_, input_character))}\n\n'  # 联想到的信息
        #           f'{HISTORY_TEMPLATE.format(content=self.st_memory.to_prompt())}\n\n'  # 最近的对话
        #           )
        #
        # # c1做出行动，c1对c2说了话，假设llm是c2，等待llm的回应
        # react_guide = (f'{HISTORY_FORMAT}\n\n'  # 通用prompt告诉llm用固定格式返回
        #                + REACT_TEMPLATE.format(
        #             c2=self.character.name,
        #             message=Message(from_character=input_character.name,
        #                             to_character=self.character.name,
        #                             action=input_.action,
        #                             message=input_.message)))

        get_logger().debug(f"react prompt: \n{prompt}")
        get_logger().debug(f"react guide: \n{react_guide}")

        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(react_guide)

        get_logger().info(f'react return:{ret}\n')
        message = Message.parse_raw(ret)
        # 记录到history
        self.record(input_character, input_, message)

        return message

    def long_term_plan(self, steps_of_plan: int):
        """机器人的大脑具备计划能力，他可以根据目前的情况规划出之后需要做的事情"""
        self.latest_long_term_plan = self.plan_ability.long_term_ability(steps_of_plan)
        return self.latest_long_term_plan

    def short_term_plan(self):
        """机器人具备短期计划的能力，他可以根据目前的情况和长期计划规划出下一步需要做的事情"""
        return self.plan_ability.short_term_ability(self.latest_long_term_plan)

    def record(self, character_input: Character, message_in: Message, message_out: Message):
        """机器人大脑记录信息"""
        self.feed_history(character_input, message_in, message_out)

    def search_relative_memory(self, key_word):
        return self.lt_memory.search(key_word)

    def get_relative_memory_prompt(self, key_word):
        return "\n".join(self.search_relative_memory(key_word))

    def conclude(self, history_list: List[History]):
        """机器人的大脑具备总结的能力，
        你给他一段交互历史，他可以用一段话总结出概要，
        并存储到长期记忆内"""

        conclusion = self.conclude_ability.conclude(history_list)
        self.lt_memory.save(conclusion)

        # 标记已经被总结过的history，这里没法做成事务，但是无所谓，long term memory可以接受低概率的重复
        self.st_memory.batch_set_history_remembered([history.id for history in history_list])

    def feed_history(self, character_input: Character, message_in: Message, message_out: Message):
        self.st_memory.add(character_input, message_in, message_out)
        history_list = self.st_memory.shrink()
        if len(history_list) > 0:
            self.conclude(history_list)
