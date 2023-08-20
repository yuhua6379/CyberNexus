from typing import List

from langchain.tools import BaseTool

from bot.base_bot import BaseBot
from common.base_thread import get_logger
from model.base_prompt_factory import BasePromptFactory
from model.llm import BaseLLM
from repo.character import Character


class SelfDriveBot(BaseBot):
    """自驱动bot，可以被唤醒去规划自己的下一个议程"""

    def __init__(self, llm: BaseLLM, character: Character, factory: BasePromptFactory):
        BaseBot.__init__(self, llm, character, factory)

    def wake(self, situation):
        super().wake(situation)
        self.reschedule()

    def reschedule(self):
        self.brain.schedule()

    def make_impression(self, character: Character):
        self.brain.impress(character)
