from typing import List

from bot.agent import AgentBuilder
from bot.brain.ablity.conclude import ConcludeAbility
from bot.brain.ablity.schedule import ScheduleAbility
from bot.brain.longterm_memory import LongTermMemory
from bot.brain.shorterm_memory import ShortTermMemory
from bot.config.base_conf import MAX_SHORT_TERM_MEMORY, HISTORY_TEMPLATE, \
    REACT_TEMPLATE, HISTORY_FORMAT, STARTCHAT_TEMPLATE
from bot.message import Message
from common.base_thread import get_logger
from repo.character import Character
from repo.history import History
from repo.scheudle import Schedule, SCHEDULE_COUNT


class Brain:

    def __init__(self, character: Character, llm_agent_builder: AgentBuilder):
        self.character = character
        self.lt_memory = LongTermMemory(character)
        self.st_memory = ShortTermMemory(max_length=MAX_SHORT_TERM_MEMORY, character=character)
        self.llm_agent_builder = llm_agent_builder
        self.conclude_ability = ConcludeAbility(self.llm_agent_builder, self.character)

        self.schedule_ability = ScheduleAbility(self.llm_agent_builder, self.character, self.st_memory,
                                                self.lt_memory)

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
        ret = (f"{self.lt_memory.relative_memory_to_prompt(key_word=kw1, limit=2)}\n"
               f"{self.lt_memory.relative_memory_to_prompt(key_word=kw2, limit=2)}").strip()
        if len(ret) == 0:
            return ""

        return ret

    def associateToCharacter(self, input_character: Character):
        """机器人大脑对外部刺激联想到某些事情"""
        # 联想的关键词，要包含input_character的名字，否则可能联想不出input_character的记忆
        kw1 = f'{input_character.name}'
        ret = (f"{self.lt_memory.relative_memory_to_prompt(key_word=kw1, limit=2)}\n").strip()
        if len(ret) == 0:
            return ""

        return ret

    def recent_memory(self):
        """机器人大脑回想起最近的信息"""
        return self.lt_memory.latest_memory_to_prompt()

    def react(self, input_: Message, input_character: Character, debug=True):
        """
        机器人大脑对外部刺激做出反应:
        1.保证机器人基础设定
        2.从输入associate一些memory
        3.使用llm处理，并作出反应
        4.记录历史到history，必要时转化为memory

        输入的内容 = 基础人物设定 + (历史的交互 + 当前的交互) + (关联memory + 最近memory) + 正在进行的plan
        """

        prompt = (f'{self.character.character_prompt}\n\n'  # 基础人物设定
                  f'{self.get_debug_prompt()}'
                  )

        # 短期记忆 = 历史的交互 + 当前的交互
        history_prompt = f'{HISTORY_TEMPLATE.format(content=self.st_memory.history_to_prompt())}\n'
        history_prompt += input_.to_prompt() + "\n" # c1 对 c2的交互

        # associate到的长期记忆
        relative_memory = self.associate(input_, input_character)

        recent_memory = self.recent_memory()

        item_doing = None
        if Schedule.get_by_character(self.character.id) is not None:
            item_doing = Schedule.get_by_character(self.character.id).item_doing

        # 引导llm回答的提示词
        react_request = REACT_TEMPLATE.format(
            c2=self.character.name,  # 假设llm是c2，等待llm的回应
            relative_memory=relative_memory,
            recent_memory=recent_memory,
            item_doing=item_doing,  # 计划去做的事情
            history=history_prompt)

        # c1做出行动，c1对c2说了话，假设llm是c2，等待llm的回应
        react_guide = (f'{HISTORY_FORMAT}\n\n'  # 通用prompt告诉llm用固定格式返回
                       + react_request)
        if debug:
            get_logger().debug(f"react prompt: \n{prompt}")
            get_logger().debug(f"react guide: \n{react_guide}")

        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(react_guide)

        if debug:
            get_logger().info(f'react return:{ret}\n')

        message = Message.parse_raw(ret)
        # 记录到history
        self.record(input_character, input_, message)

        return message

    def startInteract(self, input_character: Character, debug=True):
        """
        机器人大脑对外部刺激做出反应:
        1.保证机器人基础设定
        2.从输入associate一些memory
        3.使用llm处理，并作出反应
        4.记录历史到history，必要时转化为memory

        输入的内容 = 基础人物设定 + (历史的交互 + 当前的交互) + (关联memory + 最近memory) + 正在进行的plan
        """

        prompt = (f'{self.character.character_prompt}\n\n'  # 基础人物设定
                  f'{self.get_debug_prompt()}'
                  )

        # associate到的长期记忆
        relative_memory = self.associateToCharacter(input_character)
        recent_memory = self.recent_memory()

        item_doing = None
        if Schedule.get_by_character(self.character.id) is not None:
            item_doing = Schedule.get_by_character(self.character.id).item_doing

        # 引导llm回答的提示词
        react_request = STARTCHAT_TEMPLATE.format(
            c2=self.character.name,  # 假设llm是c2，等待llm的回应
            relative_memory=relative_memory,
            recent_memory=recent_memory,
            item_doing=item_doing,  # 计划去做的事情
        )

        # c1做出行动，c1对c2说了话，假设llm是c2，等待llm的回应
        react_guide = (f'{HISTORY_FORMAT}\n\n'  # 通用prompt告诉llm用固定格式返回
                       + react_request)

        if debug:
            get_logger().debug(f"react prompt: \n{prompt}")
            get_logger()    .debug(f"react guide: \n{react_guide}")

        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(react_guide)

        if debug:
            get_logger().info(f'react return:{ret}\n')

        message = Message.parse_raw(ret)

        return message

    def schedule(self, step: int, round_: int, left_step: int):
        """机器人的大脑具备计划能力，他可以根据目前的情况规划出之后需要做的事情"""
        schedule = Schedule.get_by_character(self.character.id)

        if schedule is None:
            # 冷启动，规划
            llm_return = self.schedule_ability.schedule(self.character, [], SCHEDULE_COUNT)

            # 安排一件正在做的item
            item_to_do = llm_return.schedule
            item_doing = llm_return.schedule[0]
            schedule = Schedule(character_id=self.character.id,
                                item_doing=item_doing,
                                items_to_do=item_to_do)
            schedule.renew(schedule)
        else:
            # 先判断真正做了的是什么
            item_done = self.schedule_ability.really_done_item(schedule.item_doing,
                                                               self.st_memory.get_history())

            if left_step == 0:
                # 这个round已经结束了，总结下最近的事情
                self.conclude(self.st_memory.shrink(shrink_all=True))

            recent_done_item = Schedule.get_recent_done_items(self.character.id) + [item_done]
            # 调整计划
            llm_return = self.schedule_ability.schedule(self.character,
                                                        recent_done_item,
                                                        SCHEDULE_COUNT)

            # 安排一件正在做的item
            item_to_do = llm_return.schedule
            item_doing = llm_return.schedule[0]

            # 标记完成item，记录
            schedule.finish_item(item_done=item_done, items_to_do=item_to_do, item_doing=item_doing)

    def record(self, character_input: Character, message_in: Message, message_out: Message):
        """机器人大脑记录信息"""
        self.feed_history(character_input, message_in, message_out)

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
