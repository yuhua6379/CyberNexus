from abc import abstractmethod
from model.entities.message import Message
from datasource.vectordb.entities import Response
from model.entities.schedule import Schedule
from model.llm_session import return_type, PromptReturn
from repo.character import Character
from repo.history import History
from repo.memory import Memory


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

    def get_max_short_item_memory(self):
        """定义短期记忆最长多少条后会被自动conclude压缩"""
        return 10

    def get_name_of_system(self):
        """定义系统角色，用于驱动角色，例如schedule、conclude"""
        return "god"

    def get_max_relative_memory(self):
        """定义相关记忆的最大条数"""
        return 4

    def get_max_schedule(self):
        """单次规划最多的item数"""
        return 8

    @return_type(Schedule)
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

    @return_type(str)
    @abstractmethod
    def on_build_conclude_prompt(self,
                                 main_character: Character,
                                 history_list: list[History]) -> PromptReturn:
        """
        :param main_character: main角色
        :param history_list: main角色未形成memory的与所有交互过角色的history
        :return:
        """
        pass

    @return_type(str)
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

    @return_type(Message)
    @abstractmethod
    def on_build_stimulus_of_character(self,
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

    @return_type(Message)
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
