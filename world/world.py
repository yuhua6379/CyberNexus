import math
from typing import Tuple

from bot.base_bot import BaseBot
from bot.self_drive_bot import SelfDriveBot
from common.base_thread import get_logger
from world.botbroker import SyncBotBroker
from world.situation import BaseSituation


class BaseWorld:

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
        self.round = math.floor(self._step / self.steps_of_round)
        self.step = self._step % self.steps_of_round

        return self.step, self.round

    def join(self, bot: BaseBot):
        """机器人通过这个方法加入到这个world内"""
        self.broker.join(bot)

        # 马上通知一次
        self._notify_bot(bot, self.step, self.round)

    def _notify_bot(self, bot: BaseBot, step: int, round_: int):
        self.broker.notify(bot, BaseSituation(step=step, round=round_))

    def run(self):
        step, round_ = self.next()
        get_logger().info(f"step: {step} round: {round_}")
        for bot in self.broker.bots.values():
            get_logger().info(f"wake bot: {bot.character.id} - {bot.character.name}")
            self._notify_bot(bot, step, round_)

    def run_until_next_round(self):
        cur_round = self.round
        while cur_round == self.round:
            self.run()


class SimpleTuneBaseWorld(BaseWorld):
    """简单朴素的回合制世界"""
    pass
