from queue import Queue
from typing import List, Any

from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool
from pydantic import BaseModel

from bot.base_bot import BaseBot
from bot.message import Message
from common.base_thread import BaseThread
from repo.character import Character


class QueueMessage(BaseModel):
    type: str
    data: Any
    return_queue: Any


class SelfDriveBot(BaseBot, BaseThread):
    """自驱动bot，会在一个后台线程里面启动"""

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character, steps_of_round: int):
        BaseBot.__init__(self, llm, tools, character)
        BaseThread.__init__(self, f"{character.name}-{character.id}")
        self.queue = Queue()
        self.lasted_situation = None
        self.steps_of_round = steps_of_round

    def wake(self, situation):
        """world的轮动会wake自驱动机器人，以触发他的自驱"""
        self.queue.put(QueueMessage(type="situation", data=situation))

    def self_drive(self, situation):
        self.log.info(situation)
        if (self.lasted_situation is not None
                and self.lasted_situation.round < situation.round):
            self.brain.long_term_plan(self.steps_of_round)
        self.brain.short_term_plan()

    def interact(self, message: Message, input_character: Character):
        queue_message_return = Queue()
        self.queue.put(QueueMessage(type="message", data=(message, input_character), return_queue=queue_message_return))
        return queue_message_return.get()

    def run(self):
        self.wait_for_awake()

    def wait_for_awake(self):
        # 启动先进行一次长期规划
        # self.brain.long_term_plan(self.steps_of_round)

        """等待world的wake"""
        while True:
            # awake并且感知到了situation
            ret: QueueMessage = self.queue.get()
            if ret.type == "situation":
                # self.self_drive(ret.data)
                pass
            if ret.type == "message":
                try:
                    res = super().interact(ret.data[0], ret.data[1])
                    ret.return_queue.put(res)
                except Exception as e:
                    ret.return_queue.put(str(e))
