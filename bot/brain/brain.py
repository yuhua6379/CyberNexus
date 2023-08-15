from collections import defaultdict
from typing import List, Optional

from model.agent import AgentBuilder
from bot.brain.ablity.conclude import ConcludeAbility
from bot.brain.ablity.longterm_memory import LongTermMemory
from bot.brain.ablity.react import ReactAbility
from bot.brain.ablity.schedule import ScheduleAbility
from bot.brain.ablity.shorterm_memory import ShortTermMemory
from model.charlie_prompt_factory import CharliePromptFactory
from model.entities.message import Message
from model.base_prompt_factory import BasePromptFactory
from model.sample_prompt_factory import SamplePromptFactory
from model.prompt_broker import PromptBroker
from repo.character import Character
from repo.history import History, Direction
from repo.scheudle import Schedule


class Brain:

    def __init__(self, character: Character, llm_agent_builder: AgentBuilder,
                 factory: BasePromptFactory = CharliePromptFactory()):
        self.broker = PromptBroker(factory)
        self.character = character
        self.llm_agent_builder = llm_agent_builder
        self.debug_prompt = ""

        self.lt_memory = LongTermMemory(character)
        self.st_memory = ShortTermMemory(
            max_length=self.broker.factory.get_max_short_item_memory(),
            character=character)

        self.conclude_ability = ConcludeAbility(self.llm_agent_builder, self.character, self.broker)

        self.schedule_ability = ScheduleAbility(self.llm_agent_builder, self.character, self.broker)

        self.react_ability = ReactAbility(
            character, self.broker, llm_agent_builder)

    # ---------------------------------场景--------------------------------- #
    def react(self, input_: Message, input_character: Character):
        """
        机器人大脑对外部刺激做出反应:
        1.保证机器人基础设定
        2.从输入associate一些memory
        3.使用llm处理，并作出反应
        4.记录历史到history，必要时转化为memory

        输入的内容 = 基础人物设定 + (历史的交互 + 当前的交互) + (关联memory + 最近memory) + 正在进行的plan
        """

        item_doing = None
        if Schedule.get_by_character(self.character.id) is not None:
            item_doing = Schedule.get_by_character(self.character.id).item_doing

        history_list = self.interact_history()
        relative_memory = self.associate(input_, input_character)
        recent_memory = self.recent_memory()
        message = self.react_ability.react(
            input_,
            input_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

        # 记录到history
        self.record(input_character, input_, message)

        return message

    def stimulus_of_character(self, input_character: Character):
        """机器人大脑受到了外部刺激，刺激对象是一个character"""
        item_doing = None
        if Schedule.get_by_character(self.character.id) is not None:
            item_doing = Schedule.get_by_character(self.character.id).item_doing

        history_list = self.interact_history_with(input_character)
        relative_memory = self.associate(None, input_character)
        recent_memory = self.recent_memory()
        message = self.react_ability.stimulus_of_character(input_character,
                                                           item_doing,
                                                           history_list,
                                                           relative_memory,
                                                           recent_memory)

        # 记录到history
        self.record(input_character, Message(from_character=input_character.name, to_character=input_character.name, stop=0), message)
        return message

    def schedule(self, step: int, round_: int, left_step: int):
        """机器人的大脑具备计划能力，他可以根据目前的情况规划出之后需要做的事情"""
        schedule = Schedule.get_by_character(self.character.id)

        if schedule is None:
            # 冷启动，规划
            llm_return = self.schedule_ability.schedule([], self.broker.factory.get_max_schedule(),
                                                        self.recent_memory())

            # 安排一件正在做的item
            item_to_do = llm_return.schedule
            item_doing = llm_return.schedule[0]
            schedule = Schedule(character_id=self.character.id,
                                item_doing=item_doing,
                                items_to_do=item_to_do)
            schedule.renew(schedule)
        else:
            # 先判断真正做了的是什么
            item_done = self.schedule_ability.determine_whether_item_finish(schedule.item_doing,
                                                                            self.interact_history(),
                                                                            self.recent_memory())

            if left_step == 0:
                # 这个round已经结束了，总结下最近的事情
                self.conclude_all(self.st_memory.shrink(shrink_all=True))

            recent_done_item = Schedule.get_recent_done_items(self.character.id) + [item_done]
            # 调整计划
            llm_return = self.schedule_ability.schedule(recent_done_item,
                                                        self.broker.factory.get_max_schedule(),
                                                        self.recent_memory())

            # 安排一件正在做的item
            item_to_do = llm_return.schedule
            item_doing = llm_return.schedule[0]

            # 标记完成item，记录
            schedule.finish_item(item_done=item_done, items_to_do=item_to_do, item_doing=item_doing)

    def remember_deeply(self, memory: str, force_to_remember=False):
        """
        机器人大脑具备长期记忆能力，但是，不是所有记忆都会记录，只能记录深刻的记忆
        :param force_to_remember: 强制去记忆，不需要rank
        :param memory:
        :return:
        """

        if force_to_remember:
            self.lt_memory.save(memory)
            return

        rank = self.conclude_ability.rank(memory)
        if rank >= self.broker.factory.get_threshold_of_rank_to_remember():
            self.lt_memory.save(memory)

    def impress(self, other_character: Character):
        """
        机器人的大脑具备总结的能力，
        你给他一段交互历史，他可以用一段话总结出他对other_character的印象，
        并存储到长期记忆内"""

        history_list = self.st_memory.get_not_impressed_history_with_character(other_character)

        impression_before = self.lt_memory.get_impression_about(other_character)
        impression_now = self.conclude_ability.impress(history_list, other_character, impression_before)
        self.lt_memory.make_impression_about(other_character, impression_now)

        # 标记印象已经形成
        self.st_memory.batch_set_history_remembered([history.id for history in history_list])

    def conclude(self, history_list: List[History], other_character: Character):
        """机器人的大脑具备总结的能力，
        你给他一段交互历史，他可以用一段话总结出概要，
        并存储到长期记忆内"""
        if len(history_list) == 0:
            return

        conclusion = self.conclude_ability.conclude(history_list, other_character)
        self.remember_deeply(conclusion)

        # 标记已经被总结过的history，这里没法做成事务，但是无所谓，long term memory可以接受低概率的重复
        self.st_memory.batch_set_history_remembered([history.id for history in history_list])

    # ---------------------------------场景--------------------------------- #

    # ---------------------------------方法--------------------------------- #

    def conclude_all(self, history_list: List[History]):
        # 总结交互
        character_history_list_dict = defaultdict(list)
        for history in history_list:
            character_history_list_dict[(history.other_character.id, history.other_character)].append(history)
        for tp, item in character_history_list_dict.items():
            history_list = item
            other_character = tp[1]

            self.conclude(history_list, other_character)

    def record(self, character_input: Character, message_in: Message, message_out: Message):
        """机器人大脑记录信息"""
        self.feed_history(character_input, message_in, message_out)

    def set_debug_prompt(self, prompt: str):
        self.debug_prompt = prompt.strip()

    def get_debug_prompt(self):
        if len(self.debug_prompt) == 0:
            return ""
        else:
            return self.debug_prompt + "\n\n"

    def associate(self, input_: Optional[Message], input_character: Character):
        """机器人大脑对外部刺激联想到某些事情"""
        if input_ is None:
            kw = f'{input_character.name}'
            return self.lt_memory.search(key_word=kw,
                                         limit=self.broker.factory.get_max_relative_memory())
        else:
            kw = f'{input_character.name}: {input_.action}: {input_.message}'
            return self.lt_memory.search(key_word=kw,
                                         limit=self.broker.factory.get_max_relative_memory())

    def interact_history(self):
        # 角色个人的所有history
        return self.st_memory.get_history()

    def interact_history_with(self, target_character: Character):
        # 角色与特定角色的history
        return self.st_memory.get_history_with_character(target_character)

    def recent_memory(self):
        """机器人大脑回想起最近的信息"""
        return self.lt_memory.latest_memory()

    @classmethod
    def make_history(cls, direction: Direction, main_character: Character, other_character: Character,
                     message_in: Message, message_out: Message):
        return History(main_character=main_character,
                       other_character=other_character,
                       main_message=message_out.message,
                       main_action=message_out.action,
                       other_message=message_in.message,
                       other_action=message_in.action,
                       direction=direction,
                       main_stop=message_in.stop,
                       other_stop=message_out.stop
                       )

    def feed_history(self, character_input: Character, message_in: Message, message_out: Message):
        history = self.make_history(Direction.to_main, self.character, character_input, message_in, message_out)
        self.st_memory.add(history)
        history_list = self.st_memory.shrink()
        if len(history_list) > 0:
            self.conclude_all(history_list)
    # ---------------------------------方法--------------------------------- #
