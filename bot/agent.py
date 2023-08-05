import logging
from typing import List

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models.base import BaseChatModel
from langchain.schema import SystemMessage
from langchain.tools import BaseTool
from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import ChatLogModel
from repo.character import Character


class Agent(BaseModel):
    prompt: str
    llm: BaseChatModel
    # agent_core: AgentExecutor
    character1: Character
    character2: Character
    version: str = '0.0.1'

    def chat(self, message_in: str) -> str:
        message_in = self.on_chat(message_in)
        # message_out = self.agent_core.run(message_in)
        message_out = self.llm.predict(self.prompt+"\n"+message_in)
        self.after_chat(message_in, message_out)

        return message_out

    def on_chat(self, input_: str) -> str:
        return input_

    def after_chat(self, message_in: str, message_out: str):
        logging.debug(f"{self.character1.name} -> {self.character2.name}: {message_in}")
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
        # prompt = OpenAIFunctionsAgent.create_prompt(system_message=SystemMessage(content=prompt))
        # langchain_agent = OpenAIFunctionsAgent(llm=self.llm, tools=self.tools, prompt=prompt)

        return Agent(llm=self.llm,
                     prompt=prompt,
                     character1=character1,
                     character2=character2)
