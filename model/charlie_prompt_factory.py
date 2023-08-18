from datasource.vectordb.entities import Response
from model.base_prompt_factory import BasePromptFactory
from model.entities.message import Message
from model.entities.schedule import Schedule
from model.llm_session import return_type, PromptReturn
from repo.character import Character
from repo.history import History
from repo.memory import Memory


class CharliePromptFactory(BasePromptFactory):
    schedule_definition = {
        "type_": Schedule,
        "title": "你必须用 JSON 格式表示角色之间的交互，具体要求如下：",
        "examples": [Schedule(schedule=["吃早餐", "去上班", "开始工作", "完成工作", "下班回家"])]
    }

    message_definition = {
        "title": "You should provide a valid RFC8259 compliant JSON response, including only the following parameters: ",
        "examples": [],
        "type_": Message,
        "example_title": "You should think step by step:"
                         "Step 1. 生成一个json格式的对话；\n Step 2. 调整 json 保证格式正确，不包含其他参数；\n Step 3. 如果生成的 message 和已有内容重复或相似，就重新生成；\n Step 4. 如果你感觉对话可以结束（2 of 10），请将 stop 设置为 1，否则设置为 0。",

    }

    @return_type(**schedule_definition)
    def on_build_schedule_prompt(self, main_character: Character, item_done: list[str], steps: int,
                                 recent_memory: list[Memory]):
        scheduling_template = '''角色设定:
            """{character_setting}"""

            这是一些最近的记忆:
            """{memory}"""

            """{schedule_format}"""

            这是你已完成的事项:
            """{item_done}"""
            请你回应1个计划，包含不超过{steps}个的步骤。
            你回应的计划必须符合角色设定。
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
        rank_template = '''请在1至10的刻度上，对下述记忆的重要性进行评估。其中，1代表日常琐事（如刷牙，铺床），而10则代表深远影响（如分手，大学录取）,如果你认为这个记忆不重要或者不符合要求，请输出0。
        记忆描述："""{memory}"""
        请评定此记忆的深度(rank)，输出一个整数。
        <填写>.
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
        conclude_template = '''这是最近的交互:
            """{history}"""

            请你用一段长度合适的话总结一下这段交互内容，注意不要遗漏重要的细节。
            '''

        kwargs = {
            "history": "\n".join([history.to_prompt(simple_string=True) for history in history_list]),
        }

        return PromptReturn(prompt_template=conclude_template,
                            kwargs=kwargs)

    @return_type(str)
    def on_build_impress_prompt(self, main_character: Character, other_character: Character,
                                history_list: list[History], impression_before: str) -> PromptReturn:
        impression_template = '''这是你和"{other_character}"的之前的互动记录： 
                    """{history}"""

                    总结一下你对"{other_character}"的印象(impression)，输出一个100个字以内的字符串，尽量包含重要细节。
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

        determine_whether_item_finish_template = '''角色设定:
                            """{character_setting}"""
                
                            这是一些最近的记忆:
                            """{memory}"""
                
                            这是你计划做的事情，但这事情可能受到干扰未必会完成:
                            """{item}"""
                
                            这是最近的交互:
                            """{history_string}"""
                
                            请你用一句话总结一下你最近真正做的事情。
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
    def on_build_provoked_by_character(self,
                                       main_character: Character,
                                       other_character: Character,
                                       item_doing: str,
                                       history_list: list[History],
                                       relative_memory: list[Response],
                                       recent_memory: list[Memory]):
        react_template = '''假设你是"{main_character}"，你需要决定是否和"{other_character}"进行互动以及开场语的内容是什么。
        
                            以下是所有的背景信息：
                            ---
                            这是你的角色设定:
                            """{character_setting}"""
                            
                            你正在处理的事项:
                            """{item_doing}"""
                            
                            你最近的记忆：
                            """{recent_memory}"""
                            
                            你对{other_character}的相关记忆:
                            """{relative_memory}"""
                            
                            {other_character}的外表特征:
                            """{other_character_appearance}"""
                            ---

                            {history_format}
                             
                            假设你现在遇见{other_character}，请生成对{other_character}的开场语和动作：<填写>
                            如果决定不互动，则直接回复 “不互动”。
                            '''

        kwargs = {
            "item_doing": item_doing,
            "character_setting": main_character.character_prompt,
            "relative_memory": "\n".join([doc.document.content for doc in relative_memory]).strip(),
            "recent_memory": "\n".join([memory.content for memory in recent_memory]).strip(),
            "history": "\n".join([history.to_prompt() for history in history_list]),
            "main_character": main_character.name,
            "other_character": other_character.name,
            "other_character_appearance": other_character.character_appearance
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
        react_template = '''你是"{main_character}"，你需要决定是否继续互动，如果要互动，那么你需要简洁而自然的推动对话发展。
                            
                            以下是所有的背景信息：
                            ---
                            这是你的角色设定:
                            """{character_setting}"""
                            
                            你正在处理的事项:
                            """{item_doing}"""
                            
                            你的相关记忆:
                            """{relative_memory}"""
                            
                            其他角色的外表特征:
                            """{other_character_appearance}"""
                            ---
                            
                            下面是已有的对话内容:
                            """{history}"""
                            
                            {history_format}
                            
                            如果决定互动的话，请生成对"{other_character}"的动作和对话内容，请保证对话简要自然：<填写>
                            '''
        kwargs = {
            "item_doing": item_doing,
            "character_setting": main_character.character_prompt,
            "relative_memory": "\n".join([doc.document.content for doc in relative_memory]).strip(),
            "recent_memory": "\n".join([memory.content for memory in recent_memory]).strip(),
            "history": "\n".join([history.to_prompt() for history in history_list] + [input_.to_prompt()]),
            "main_character": main_character.name,
            "other_character": other_character.name,
            "other_character_appearance": other_character.character_appearance
        }

        return PromptReturn(prompt_template=react_template,
                            kwargs=kwargs,
                            position="history_format")
