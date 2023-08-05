from queue import Queue
from typing import List

from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool

from bot.base_bot import BaseBot
from common.base_thread import BaseThread
from repo.character import Character


class SelfDriveBot(BaseBot, BaseThread):
    """自驱动bot，会在一个后台线程里面启动"""

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character):
        BaseBot.__init__(self, llm, tools, character)
        BaseThread.__init__(self, f"{character.name}-{character.id}")
        self.queue = Queue()

    def wake(self, situation):
        """world的轮动会wake自驱动机器人，以触发他的自驱"""
        self.queue.put(situation)

    def self_drive(self, situation):
        self.log.info(situation)
        self.brain.short_term_plan()

    def run(self):
        self.wait_for_awake()

    def wait_for_awake(self):
        """等待world的wake"""
        while True:
            # awake并且感知到了situation
            situation = self.queue.get()
            self.self_drive(situation)
