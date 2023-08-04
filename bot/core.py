import logging
from typing import List

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models.base import BaseChatModel
from langchain.schema import SystemMessage
from langchain.tools import BaseTool
from pydantic import BaseModel

from bot.config.base_conf import base_prompt, conclude_prompt_template, title_of_relative_memory, \
    title_of_history, name_of_god, max_short_term_memory
from bot.memory.longterm_memory import LongTermMemory
from bot.memory.shorterm_memory import ShortTermMemory
from bot.prompt_factory.core import PromptFactory
from datasource.config import rdbms_instance
from datasource.rdbms.entities import ChatLogModel
from repo.character import Character


class Agent(BaseModel):
    agent_core: AgentExecutor
    character1: Character
    character2: Character
    version: str = '0.0.1'

    def chat(self, message_in: str) -> str:
        message_in = self.on_chat(message_in)
        message_out = self.agent_core.run(message_in)
        self.after_chat(message_in, message_out)

        return message_out

    def on_chat(self, input_: str) -> str:
        return input_

    def after_chat(self, message_in: str, message_out: str):
        logging.debug(f"{self.character1.name} -> {self.character1.name}: {message_in}")
        logging.debug(f"{self.character2.name} -> {self.character1.name}: {message_out}")

        log = ChatLogModel()
        log.character1_id = self.character1.id
        log.character2_id = self.character2.id
        log.character1_message = message_in
        log.character2_message = message_out

        # 记录agent的版本，便于筛选数据
        log.version = self.version

        with rdbms_instance.get_session() as session:
            session.add(log)
            session.commit()


class AgentBuilder:

    def __init__(self, llm: BaseChatModel,
                 tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools

    def build(self, prompt: str, character1: Character, character2: Character) -> Agent:
        prompt = OpenAIFunctionsAgent.create_prompt(system_message=SystemMessage(content=prompt))
        langchain_agent = OpenAIFunctionsAgent(llm=self.llm, tools=self.tools, prompt=prompt)

        return Agent(character1=character1,
                     character2=character2,
                     agent_core=AgentExecutor(agent=langchain_agent, tools=self.tools))


class Brain:

    def __init__(self, character: Character, llm_agent_builder: AgentBuilder):
        self.character = character
        self.lt_memory = LongTermMemory(character)
        self.st_memory = ShortTermMemory(max_length=max_short_term_memory, character=character)
        self.llm_agent_builder = llm_agent_builder

    def associate(self, input_: str):
        """机器人大脑对外部刺激联想到某些事情"""
        return (f"{self._get_relative_memory_prompt(title=title_of_relative_memory, key_word=input_)}\n\n"
                + self.st_memory.to_prompt(title=title_of_history))

    def react(self, input_: str, input_character: Character):
        """
        机器人大脑对外部刺激做出反应:
        1.保证机器人基础设定
        2.从输入associate一些memory
        3.使用llm处理，并作出反应
        4.记录历史到history，必要时转化为memory
        """

        # 联想的关键词，要包含input_character的名字，否则可能联想不出input_character的记忆
        associate_key_word = f'{input_character.name}: {input_}'

        factory = PromptFactory(character=self.character.character_prompt)
        prompt = f'{factory.build()}\n\n{self.associate(associate_key_word)}\n\n'

        logging.debug(f"react prompt: \n{prompt}")

        agent = self.llm_agent_builder.build(prompt=prompt,
                                             character1=input_character,
                                             character2=self.character)
        ret = agent.chat(input_)

        # 记录到history
        self.record(input_character, input_, ret)

        return ret

    def record(self, character_input: Character, message_in: str, message_out: str):
        """机器人大脑记录信息"""
        self._feed_history(character_input, message_in, message_out)

    def _search_relative_memory(self, key_word):
        return self.lt_memory.search(key_word)

    def _get_relative_memory_prompt(self, title, key_word):
        return f'{title}:\n' + "\n".join(self._search_relative_memory(key_word))

    def _feed_history(self, character_input: Character, message_in: str, message_out: str):
        self.st_memory.add(character_input, message_in, message_out)
        history_list = self.st_memory.shrink()
        if len(history_list) > 0:
            history_string = "\n".join([str(history) for history in history_list])
            logging.debug("concluding...\n" + history_string)
            conclude_prompt = conclude_prompt_template.format(history=history_string)

            # 上帝模式，没有任何多余的prompt，例如角色设定等，仅仅使用原始Agent
            god = Character.get_by_name(name_of_god)
            agent = self.llm_agent_builder.build(prompt=base_prompt,
                                                 character1=god,
                                                 character2=self.character)

            # 把总结的history形成memory放到long term memory里面
            concluded_memory = agent.chat(conclude_prompt)
            self.lt_memory.save(concluded_memory)

            # 标记已经被总结过的history，这里没法做成事务，但是无所谓，long term memory可以接受低概率的重复
            self.st_memory.batch_set_history_remembered([history.id for history in history_list])


class Bot:

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character):
        self.brain = Brain(character, AgentBuilder(llm=llm, tools=tools))

    def interact(self, input_: str, input_character: Character):
        return self.brain.react(input_, input_character)
