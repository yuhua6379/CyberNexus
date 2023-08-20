from typing import Dict

from bot.base_bot import BaseBot
from bot.self_drive_bot import SelfDriveBot
from world.situation import BaseSituation


class SyncBotBroker:

    def __init__(self):
        self.bots: Dict[int, BaseBot] = {}

    def join(self, bot: BaseBot):
        if bot in self.bots:
            return
        self.bots[bot.character.id] = bot

    # @abstractmethod
    def notify(self, bot: BaseBot, situation: BaseSituation):
        bot.wake(situation)
