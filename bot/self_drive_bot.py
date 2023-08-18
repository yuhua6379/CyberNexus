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
        self.lasted_situation = None
        self.steps_of_round = None

    def set_steps_of_round(self, steps_of_round: int):
        self.steps_of_round = steps_of_round

    def wake(self, situation):
        """world的轮动会wake自驱动机器人，以触发他的自驱"""

        # awake并且感知到了situation
        self.self_drive(situation)
        self.lasted_situation = situation

    def self_drive(self, situation):
        left_step = self.steps_of_round - situation.step
        get_logger().info(f"self_drive situation={situation} left_step={left_step}")
        self.brain.schedule(situation.step, situation.round, left_step)

    def make_impression(self, character: Character):
        self.brain.impress(character)
