from abc import abstractmethod

from datasource.vectordb.entities import Response
from model.entities.message import Message
from model.entities.schedule import Schedule
from model.llm_session import build_prompt_event, PromptReturn, build_prompt_phase, LLMSession
from repo.character import Character
from repo.history import History
from repo.memory import Memory
from world.situation import BaseSituation


class BasePromptFactory:
    """
    术语定义：
    main角色，当前bot扮演的角色
    other角色，当前bot正在交互的角色
    memory，长期记忆
    history，交互记录
    item，日程
    round，回合，例如 1天 = 1 round
    step，步骤，例如 24小时 = 24 steps
    """

    def __init__(self):
        self.debug_prompt = None

    def set_debug_prompt(self, debug_prompt):
        self.debug_prompt = debug_prompt

    def get_debug_prompt(self):
        return self.debug_prompt

    def get_max_short_item_memory(self):
        """定义短期记忆最长多少条后会被自动conclude压缩"""
        return 10

    def get_threshold_of_rank_to_remember(self):
        """定义什么深度的记忆才去记录"""
        return 5

    def get_name_of_system(self):
        """定义系统角色，用于驱动角色，例如schedule、conclude"""
        return "god"

    def get_max_relative_memory(self):
        """定义相关记忆的最大条数"""
        return 4

    def get_max_schedule(self):
        """单次规划最多的item数"""
        return 8

    @build_prompt_event(Schedule)
    @abstractmethod
    def on_build_schedule_prompt(self, main_character: Character,
                                 item_done: list[str],
                                 steps: int,
                                 recent_memory: list[Memory]) -> PromptReturn:
        """
        :param main_character: main角色
        :param item_done: main角色当前完成的item
        :param steps: 本次规划的item数
        :param recent_memory: main角色最近的lt_memory
        :return:
        """
        pass

    @build_prompt_event(str)
    @abstractmethod
    def on_build_conclude_prompt(self,
                                 main_character: Character,
                                 other_character: Character,
                                 history_list: list[History]) -> PromptReturn:
        """
        :param other_character: other角色
        :param main_character: main角色
        :param history_list: main角色未形成memory的与所有交互过角色的history
        :return:
        """
        pass

    @build_prompt_event(str)
    @abstractmethod
    def on_build_impress_prompt(self,
                                main_character: Character,
                                other_character: Character,
                                history_list: list[History],
                                impression_before: str) -> PromptReturn:
        """
        :param impression_before: main角色对other角色之前的impression
        :param other_character: other角色
        :param main_character: main角色
        :param history_list: main角色未形成memory的与所有交互过角色的history
        :return:
        """
        pass

    @build_prompt_event(int)
    @abstractmethod
    def on_build_rank_prompt(self, memory: str):
        """
        :type memory: 某角色的记忆
        """
        pass

    @build_prompt_event(str)
    @abstractmethod
    def on_build_determine_whether_item_finish_prompt(self,
                                                      main_character: Character,
                                                      target_item: str,
                                                      history_list: list[History],
                                                      recent_memory: list[Memory]) -> PromptReturn:
        """
        :param main_character: main角色
        :param target_item: 一个item，需要确定这个item是不是真正被完成了亦或是被干扰了
        :param history_list: main角色未形成memory的与所有交互过角色的history
        :param recent_memory: 最近压缩history形成的memory，并非相关的memory
        :return:
        """
        pass

    @build_prompt_event(Message)
    @abstractmethod
    def on_build_provoked_by_character(self,
                                       main_character: Character,
                                       other_character: Character,
                                       item_doing: str,
                                       history_list: list[History],
                                       relative_memory: list[Response],
                                       recent_memory: list[Memory]) -> PromptReturn:
        """
        :param item_doing: main角色正在计划做的事情
        :param main_character: mian角色
        :param other_character: other角色
        :param history_list: mian角色与other角色未形成memory的history
        :param relative_memory: 与other角色相关的memory
        :param recent_memory: main角色最近的memory
        :return:
        """
        pass

    @build_prompt_event(Message)
    @abstractmethod
    def on_build_react_prompt(self,
                              main_character: Character,
                              other_character: Character,
                              input_: Message,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]) -> PromptReturn:
        """
        :param main_character: main角色
        :param other_character: other角色
        :param input_: other角色发送给main角色的交互
        :param item_doing: main角色计划里正要做的事情
        :param history_list: mian角色与other角色未形成memory的history
        :param relative_memory: 与other角色相关的memory
        :param recent_memory: main角色最近的memory
        :return:
        """
        pass

    @build_prompt_event(str)
    def on_build_do_something_prompt(self, main_character: Character, something_to_do: str):
        """

        :param main_character: main角色
        :param something_to_do: 一件事情，例如查一下今天的天气
        :return:
        """
        do_something_template = '''
        注意！你的回应必须包含角色的名字且必须适当体现角色的特点，且你的回应一定要简洁
        
        角色设定:
        """{character_setting}"""
        
        假设你是{main_character}现在需要你去做下面这件事:
        """{something_to_do}"""
        
        然后，简洁地总结一下你所做的事情，请以第三方的角度去描述这件事情，你不能回应多余的内容，你只可以专注于所做的事情，注意不可以照抄例子，要以实际做的事情为准，例子:
        """{main_character}喝了咖啡，并且写完了代码"""
        '''

        kwargs = {
            "character_setting": main_character.character_prompt,
            "main_character": main_character.name,
            "something_to_do": something_to_do
        }

        return PromptReturn(prompt_template=do_something_template,
                            kwargs=kwargs)

    @build_prompt_phase
    def on_build_world_environment_prompt(self, event_name: str, situation: BaseSituation):
        # import random
        # print(event_name, situation)
        # if random.randint(0, 3) == 0:
        #     print("下大雨了！")
        #     return PromptReturn(prompt_template="注意！这个时候下起了大雨！", kwargs={})
        return None

    def before_call_llm(self, event_name: str, llm_session: LLMSession):
        return llm_session
