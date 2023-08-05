import math
from abc import abstractmethod
from typing import Tuple


class BaseRoundController:
    def __init__(self, steps_count_of_round):
        self.steps_count_of_round = steps_count_of_round
        self.rounds = 0
        self.steps = 0

    @abstractmethod
    def wait(self):
        pass

    def next(self) -> Tuple[int, int]:
        # 每次step + 1
        self.steps += 1
        # 重新计算第几round
        self.rounds = math.ceil(self.steps / self.steps_count_of_round)

        self.wait()

        return self.steps, self.rounds
