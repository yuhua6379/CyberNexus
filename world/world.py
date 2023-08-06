from typing import Dict

from bot.self_drive_bot import SelfDriveBot
from common.base_thread import BaseThread
from world.round_controller.time_base_controller import BaseRoundController
from world.situation import BaseSituation


class BaseWorld(BaseThread):

    def __init__(self, round_controller: BaseRoundController, logger_name):
        super().__init__(logger_name)
        self.bots: Dict[int, SelfDriveBot] = {}
        self.round_controller = round_controller

    def join(self, bot: SelfDriveBot):
        """机器人通过这个方法加入到这个world内"""
        if bot in self.bots:
            return
        self.bots[bot.character.id] = bot

    # @abstractmethod
    def wake_bot(self, bot: SelfDriveBot, step: int, round_: int):
        bot.wake(BaseSituation(step=step, round=round_))

    def run(self):
        while True:
            step, round_ = self.round_controller.next()
            self.log.info(f"step: {step} round: {round_}")
            for bot in self.bots.values():
                self.log.info(f"wake bot: {bot.character.id} - {bot.character.name}")
                self.wake_bot(bot, step, round_)
