from abc import abstractmethod
from typing import List, Optional
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.tools import BaseTool
from pydantic import BaseModel
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from bot.config.base_prompt import get_base_prompt
from datasource.rdbms.sqlite import get_session, ChatLog


class Bot(BaseModel):
    agent_core: AgentExecutor
    version: str = '0.0.1'

    def chat(self, input_: str) -> str:
        input_ = self.on_chat(input_)
        output_ = self.agent_core.run(input_)
        self.after_chat(input_, output_)

        return output_

    def on_chat(self, input_: str) -> str:
        return input_

    def after_chat(self, input_: str, output_: str):
        log = ChatLog()
        log.user = input_
        log.bot = output_
        # 记录agent的版本，便于筛选数据
        log.version = self.version
        session = get_session()
        session.add(log)
        session.commit()


class BotBuilder(BaseModel):
    llm: BaseChatModel
    tools: List[BaseTool]
    prompt: str

    @staticmethod
    def build(llm: BaseChatModel, tools: List[BaseTool], prompt: Optional[str] = None) -> Bot:
        if prompt is None:
            prompt = get_base_prompt(simple=True)
        if isinstance(llm, ChatOpenAI):
            system_message = SystemMessage(
                content=prompt)
            prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
            agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
            return Bot(agent_core=AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True))
        else:
            raise Exception(f"unknown llm type: {type(llm)}")
