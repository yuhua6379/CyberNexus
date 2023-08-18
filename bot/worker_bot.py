from typing import List

from langchain.agents import BaseSingleActionAgent
from langchain.tools import BaseTool

from bot.base_bot import BaseBot
from bot.body.body import Body
from common.base_thread import get_logger
from model.base_prompt_factory import BasePromptFactory
from model.llm import BaseLLM
from repo.character import Character


class WorkerBot(BaseBot):
    """这个机器人有自己的四肢，可以调用工具做事情"""

    def __init__(self, llm: BaseLLM, character: Character, factory: BasePromptFactory, agent: BaseSingleActionAgent, tools: List[BaseTool]):
        super().__init__(llm, character, factory)
        self.body = Body(character, agent, tools)

    def do_something(self, something_to_do):
        return self.body.do_something(something_to_do)
