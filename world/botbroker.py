from typing import Dict

from bot.self_drive_bot import SelfDriveBot
from world.situation import BaseSituation


class SyncBotBroker:

    def __init__(self):
        self.bots: Dict[int, SelfDriveBot] = {}

    def join(self, bot: SelfDriveBot):
        if bot in self.bots:
            return
        self.bots[bot.character.id] = bot

    # @abstractmethod
    def wake_bot(self, bot: SelfDriveBot, step: int, round_: int):
        bot.wake(BaseSituation(step=step, round=round_))
