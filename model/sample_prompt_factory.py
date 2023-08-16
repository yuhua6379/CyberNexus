from datasource.vectordb.entities import Response
from model.base_prompt_factory import BasePromptFactory
from model.entities.message import Message
from model.entities.schedule import Schedule
from model.llm_session import return_type, PromptReturn
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class SamplePromptFactory(BasePromptFactory):
    schedule_definition = {
        "type_": Schedule,
        "title": "你必须用 JSON 格式表示角色之间的交互，具体要求如下：",
        "examples": [Schedule(schedule=["吃早餐", "去上班", "开始工作", "完成工作", "下班回家"])]
    }

    message_definition = {
        "title": "你必须用 JSON 格式表示角色之间的交互，具体要求如下：",
        "type_": Message,
        "example_title": "let's think step by step:"
                         "1. 生成一个json格式的对话；"
                         "2. 核实 json 格式，确保格式合法。",
        "examples": [
            Message(from_character="lisa", to_character="tom", action="看了看天空，并对 tom 说道",
                    message="今天天气真不错，你不觉得吗？", stop=0),
            Message(from_character="tom", to_character="jack", action="一脸焦躁",
                    message="我必须走了，不然赶不上3点半的火车了", stop=1)
        ]
    }

    @return_type(**schedule_definition)
    def on_build_schedule_prompt(self, main_character: Character, item_done: list[str], steps: int,
                                 recent_memory: list[Memory]):
        scheduling_template = '''
            角色设定:
            {character_setting}
            
            这是一些最近的记忆:
            {memory}

            {schedule_format}

            这是你已完成的事项:
            {item_done}
            请你回应1个计划，包含{steps}个步骤
            你回应的计划，必须符合角色设定
            '''

        memory_string = "\n".join([memory.content for memory in recent_memory])
        kwargs = {
            "character_setting": main_character.character_prompt,
            "memory": memory_string,
            "item_done": "\n".join(item_done),
            "steps": steps
        }

        # 告诉底层，使用scheduling_template模板，kwargs是参数，把Schedule的定义放在schedule_format处
        return PromptReturn(prompt_template=scheduling_template,
                            kwargs=kwargs,
                            position="schedule_format")

    @return_type(int)
    def on_build_rank_prompt(self, memory: str):
        rank_template = '''
        请在1至10的刻度上，对下述记忆的重要性进行评估。其中，1代表日常琐事（如刷牙，铺床），而10则代表深远影响（如分手，大学录取）。
        记忆描述：{memory}
        请评定此记忆的深度(rank)，输出一个整数
        '''

        kwargs = {
            "memory": memory,
        }

        return PromptReturn(prompt_template=rank_template,
                            kwargs=kwargs)

    @return_type(str)
    def on_build_conclude_prompt(self,
                                 main_character: Character,
                                 other_character: Character,  # 对应的交互角色
                                 history_list: list[History]):
        conclude_template = '''
            这是最近的交互:
            {history}

            请你用一段长度适中的话总结一下这段交互，而且你只能输出这句话
            '''

        kwargs = {
            "history": "\n".join([history.to_prompt(simple_string=True) for history in history_list]),
        }

        return PromptReturn(prompt_template=conclude_template,
                            kwargs=kwargs)

    @return_type(str)
    def on_build_impress_prompt(self, main_character: Character, other_character: Character,
                                history_list: list[History], impression_before: str) -> PromptReturn:
        impression_template = '''
                    这是你和{other_character}的之前的互动记录： 

                    ---
                    {history}
                    ---
                    
                    总结一下你对{other_character}的印象(impression)，输出一个100个字以内的字符串
                    '''

        kwargs = {
            "history": "\n".join([history.to_prompt(simple_string=True) for history in history_list]),
            "other_character": other_character.name
        }

        return PromptReturn(prompt_template=impression_template,
                            kwargs=kwargs)

    @return_type(str)
    def on_build_determine_whether_item_finish_prompt(self,
                                                      main_character: Character,
                                                      target_item: str,
                                                      history_list: list[History],
                                                      recent_memory: list[Memory]):
        """输入内容 = 基础人物设定 + 最近的memory + 最近的交互 + 正在计划做的事情"""

        determine_whether_item_finish_template = '''
            角色设定:
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

    @return_type(**message_definition)
    def on_build_stimulus_of_character(self,
                                       main_character: Character,
                                       other_character: Character,
                                       item_doing: str,
                                       history_list: list[History],
                                       relative_memory: list[Response],
                                       recent_memory: list[Memory]):
        react_template = '''
                            角色设定:
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
                            现在，假设你是{main_character}
                            假设你现在遇见{other_character}，请生成对{other_character}的回复：<填写>
                            '''

        kwargs = {
            "item_doing": item_doing,
            "character_setting": main_character.character_prompt,
            "relative_memory": "\n".join([doc.document.content for doc in relative_memory]).strip(),
            "recent_memory": "\n".join([memory.content for memory in recent_memory]).strip(),
            "history": "\n".join([history.to_prompt() for history in history_list]),
            "main_character": main_character.name,
            "other_character": other_character.name
        }

        return PromptReturn(prompt_template=react_template,
                            kwargs=kwargs,
                            position="history_format")

    @return_type(**message_definition)
    def on_build_react_prompt(self,
                              main_character: Character,
                              other_character: Character,
                              input_: Message,
                              item_doing: str,
                              history_list: list[History],
                              relative_memory: list[Response],
                              recent_memory: list[Memory]):
        react_template = '''
                                    角色设定:
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
                                    注意！！你生成的内容必须不能跟交互记录相似，必须不同
                                    现在，假设你是{main_character}
                                    请生成对{other_character}的回复：<填写>
                                    '''
        kwargs = {
            "item_doing": item_doing,
            "character_setting": main_character.character_prompt,
            "relative_memory": "\n".join([doc.document.content for doc in relative_memory]).strip(),
            "recent_memory": "\n".join([memory.content for memory in recent_memory]).strip(),
            "history": "\n".join([history.to_prompt() for history in history_list] + [input_.to_prompt()]),
            "main_character": main_character.name,
            "other_character": other_character.name
        }

        return PromptReturn(prompt_template=react_template,
                            kwargs=kwargs,
                            position="history_format")
