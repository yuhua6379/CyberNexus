import math
from typing import Tuple

from bot.self_drive_bot import SelfDriveBot
from common.base_thread import get_logger
from world.botbroker import SyncBotBroker


class TurnBaseWorld:

    def __init__(self, steps_of_round: int, broker: SyncBotBroker):
        self.broker = broker

        self.steps_of_round = steps_of_round
        self.round = 0
        self._step = 0
        self.step = 0

    def next(self) -> Tuple[int, int]:
        # 每次step + 1
        self._step += 1
        # 重新计算第几round
        self.round = math.ceil(self._step / self.steps_of_round)
        self.round = self._step % self.steps_of_round

        return self.step, self.round

    def join(self, bot: SelfDriveBot):
        """机器人通过这个方法加入到这个world内"""
        bot.set_steps_of_round(self.steps_of_round)
        self.broker.join(bot)

    # @abstractmethod
    def _wake_bot(self, bot: SelfDriveBot, step: int, round_: int):
        self.broker.wake_bot(bot, step, round_)

    def run(self):
        step, round_ = self.next()
        get_logger().info(f"step: {step} round: {round_}")
        for bot in self.broker.bots.values():
            get_logger().info(f"wake bot: {bot.character.id} - {bot.character.name}")
            self._wake_bot(bot, step, round_)
