import os
from typing import List

import openai
from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool
from pydantic import BaseModel

from common.base_thread import get_logger
from datasource.config import rdbms_instance
from datasource.rdbms.entities import ChatLogModel
from repo.character import Character


def complete(prompt):
    messages = [
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 选择适当的引擎
        messages=messages,
        temperature=0
    )

    if response['choices'][0]['message']:
        return response['choices'][0]['message']['content'].strip()
    else:
        return ''


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
        final_message = self.prompt + "\n\n" + message_in

        # message_out = self.llm.predict(final_message)
        openai.api_key = os.environ['open_ai_key']
        message_out = complete(final_message)
        get_logger().debug(f"[[final message]]: {final_message}")
        self.after_chat(message_in, message_out)

        return message_out

    def on_chat(self, input_: str) -> str:
        return input_

    def after_chat(self, message_in: str, message_out: str):
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
