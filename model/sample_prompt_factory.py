from model.entities.message import Message
from common.base_thread import get_logger
from datasource.vectordb.entities import Response
from model.base_prompt_factory import BasePromptFactory
from model.entities.schedule import Schedule
from model.llm_session import return_type, pydantic2prompt, PromptReturn
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class SamplePromptFactory(BasePromptFactory):
    HISTORY_FORMAT = '''
    你需要完成接下来的一系列对话，要求如下：
    你必须用 JSON 格式表示角色之间的交互，具体要求如下：
    - "from_character": 代表发出动作或消息的角色。
    - "to_character": 代表接收动作或消息的角色。
    - "action": 此参数为可选，表示角色做出的动作。此处不能使用“我”，而应使用具体名字。若无动作，则不加入此参数。
    - "message": 此参数为可选，表示角色所说的话或者自言自语。不可用于陈述行动。若不需说话，则不加入此参数。
    - "message" 和 "action" 中至少要有一个。
    - "stop": 此参数意味着from_character代表的角色觉得对话已经结束，无需再进行回复。若无此参数，则默认为0，即对话未结束。

    示例1：
    {
        "from_character": "lisa",
        "to_character": "tom",
        "action": "看了看天空，并对 tom 说道",
        "message": "今天天气真不错，你不觉得吗？",
        "stop": 0
    }

    示例2：
    {
        "from_character": "tom",
        "to_character": "jack",
        "action": "一脸焦躁",
        "message": "我必须走了，不然赶不上3点半的火车了",
        "stop": 1
    }

    let's think step by step:
    1. 生成一个json格式的对话；
    2. 核实 json 格式，确保格式合法。
    比如：{
        "from_character": "hero",
        "to_character": "镇长先生",
        "action": "",
        "message": "镇长先生，非常感谢您的关心和提醒。我明白保护社区和居民的重要性，这也是我前往讨伐魔王的初衷。我会尽我; pos=93; lineno=5; colno=16)
    就不是一个合法的 json 格式。
    3. 如果格式有问题，此时你需要重新生成正确的 json 格式。

    '''

    IF_ITEM_DONE_TEMPLATE = '''
    这是一些最近的记忆:
    {memory}

    这是你计划做的事情，但这事情可能受到干扰未必会完成:
    {item}

    这是最近的交互:
    {history_string}

    请你用一句话总结一下你最近真正做的事情
    '''

    RELATIVE_MEMORY_TEMPLATE = '''以下是相关的一些记忆:\n{content}'''

    RECENT_MEMORY_TEMPLATE = '''以下是最近的一些记忆:\n{content}'''

    HISTORY_TEMPLATE = '''以下是最近的交互:\n{content}'''

    EMPTY_ACTION = ""
    EMPTY_MESSAGE = ""

    schedule_definition = {
        "type_": Schedule,
        "title": "你需要完成接下来的一系列对话，要求如下： "
                 "你必须用 JSON 格式表示角色之间的交互，具体要求如下：",
        "examples": [Schedule(schedule=["吃早餐", "出门", "上班"])]
    }

    message_definition = {
        "type_": Message,
        "title": "你需要完成接下来的一系列对话，要求如下： "
                 "你必须用 JSON 格式表示角色之间的交互，具体要求如下：",
        "examples": [
            Message(from_character="lisa", to_character="tom", action="看了看天空，并对 tom 说道",
                    message="今天天气真不错，你不觉得吗？", stop=0),
            Message(from_character="tom", to_character="jack", action="一脸焦躁",
                    message="我必须走了，不然赶不上3点半的火车了", stop=1)
        ],
        "example_title": "let's think step by step:"
                         "1. 生成一个json格式的对话；"
                         "2. 核实 json 格式，确保格式合法。"
    }

    @return_type(**schedule_definition)
    def on_build_schedule_prompt(self, main_character: Character, item_done: list[str], steps: int,
                                 recent_memory: list[Memory]):
        scheduling_template = '''
            {character_setting}
            
            这是一些最近的记忆:
            {memory}

            {schedule_format}

            这是你已完成的事项:
            {item_done}
            请你回应1个计划，包含{steps}个步骤
            '''

        memory_string = "\n".join([memory.content for memory in recent_memory])
        kwargs = {
            "character_setting": main_character.character_prompt,
            "memory": memory_string,
            "item_done": item_done,
            "steps": steps
        }

        # 告诉底层，使用scheduling_template模板，kwargs是参数，把Schedule的定义放在schedule_format处
        return PromptReturn(prompt_template=scheduling_template,
                            kwargs=kwargs,
                            position="schedule_format")

    @return_type(str)
    def on_build_conclude_prompt(self,
                                 main_character: Character,
                                 history_list: list[History]):
        conclude_template = '''
            {history_format}
            这是最近的交互:
            {history}

            请你用一段长度适中的话总结一下这段交互，而且你只能输出这句话
            '''

        kwargs = {
            "history": "\n".join([history.to_prompt() for history in history_list]),
            "history_format": pydantic2prompt(**self.message_definition)
        }

        return PromptReturn(prompt_template=conclude_template,
                            kwargs=kwargs)

    @return_type(str)
    def on_build_determine_whether_item_finish_prompt(self,
                                                      main_character: Character,
                                                      target_item: str,
                                                      history_list: list[History],
                                                      recent_memory: list[Memory]):
        """输入内容 = 基础人物设定 + 最近的memory + 最近的交互 + 正在计划做的事情"""

        determine_whether_item_finish_template = '''
            {character_setting}
            
            这是一些最近的记忆:
            {memory}

            这是你计划做的事情，但这事情可能受到干扰未必会完成:
            {item}

            这是最近的交互:
            {history_string}

            请你用一句话总结一下你最近真正做的事情
            '''

        kwargs = {
            "character_setting": main_character.character_prompt,
            "memory": "\n".join([memory.content for memory in recent_memory]),
            "item": target_item,
            "history_string": '\n'.join([history.to_prompt(True) for history in history_list])
        }

        return PromptReturn(prompt_template=determine_whether_item_finish_template,
                            kwargs=kwargs)

    @classmethod
    def common_react(cls,
                     main_character: Character,
                     other_character: Character,
                     item_doing: str,
                     history_list: list[History],
                     relative_memory: list[Response],
                     recent_memory: list[Memory]):
        react_template = '''
                    {character_setting}

                    {history_format}

                    相关的记忆:
                    {relative_memory}

                    最近的记忆:
                    {recent_memory}

                    正在进行的计划:
                    {item_doing}

                    交互记录：
                    {history}
                    请生成{other_character}的回复：<填写>
                    '''

        kwargs = {
            "item_doing": item_doing,
            "character_setting": main_character.character_prompt,
            "relative_memory": "\n".join([doc.document.content for doc in relative_memory]).strip(),
            "recent_memory": "\n".join([memory.content for memory in recent_memory]).strip(),
            "history": "\n".join([history.to_prompt() for history in history_list]),
            "other_character": other_character.name
        }

        return PromptReturn(prompt_template=react_template,
                            kwargs=kwargs,
                            position="history_format")

    @return_type(**message_definition)
    def on_build_stimulus_of_character(self,
                                       main_character: Character,
                                       other_character: Character,
                                       item_doing: str,
                                       history_list: list[History],
                                       relative_memory: list[Response],
                                       recent_memory: list[Memory]):
        return self.common_react(
            main_character,
            other_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)

    @return_type(**message_definition)
    def on_build_react_prompt(self,
                              main_character: Character,
                              other_character: Character,
                              input_: Message,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]):
        return self.common_react(
            main_character,
            other_character,
            item_doing,
            history_list,
            relative_memory,
            recent_memory)
