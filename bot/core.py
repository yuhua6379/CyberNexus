import logging
from enum import Enum
from typing import List

from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from .agent_hooker import OpenAIFunctionsAgent
from langchain.tools import BaseTool
from pydantic import BaseModel
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor

from bot.config.base_prompt import get_base_prompt
from bot.memory.shorterm_memory import ShortTermMemoryLoader
from datasource.rdbms.sqlite import get_session, ChatLogModel, CharacterModel


class Character(BaseModel, orm_mode=True):
    class CharacterType(Enum):
        bot = "bot"
        user = "user"

    id: str
    name: str
    type: CharacterType

    @classmethod
    def get_by_name(cls, name: str):
        with get_session() as session:
            result = session.query(CharacterModel).filter(CharacterModel.name == name).one()
            return Character.from_orm(result)



class Bot(BaseModel):
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
        logging.debug(message_in)
        logging.debug(message_out)

        log = ChatLogModel()
        log.character1_id = self.character1.id
        log.character2_id = self.character2.id
        log.character1_message = message_in
        log.character2_message = message_out

        # 记录agent的版本，便于筛选数据
        log.version = self.version

        with get_session() as session:
            session.add(log)
            session.commit()


class BotBuilder(BaseModel):
    llm: BaseChatModel
    tools: List[BaseTool]
    prompt: str

    @staticmethod
    def build(character1: Character, character2: Character, llm: BaseChatModel, tools: List[BaseTool], prompt: str = "") -> Bot:
        prompt = (get_base_prompt() + "\n"
                  + prompt + '\n'
                  + f"suppose i am {character1.name} and you are {character2.name}"
                  )

        if isinstance(llm, ChatOpenAI):
            system_message = SystemMessage(
                content=prompt)
            prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

            agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

            # ConversationBufferMemory
            memory = ShortTermMemoryLoader(character1_id=character1.id,
                                           character2_id=character2.id,
                                           limiter=ShortTermMemoryLoader.LengthLimiter(50))
            # memory = ConversationBufferMemory()
            return Bot(character1=character1,
                       character2=character2,
                       agent_core=
                       AgentExecutor(
                           agent=agent,
                           tools=tools,
                           verbose=True,
                           memory=memory))
        else:
            raise Exception(f"unknown llm type: {type(llm)}")
