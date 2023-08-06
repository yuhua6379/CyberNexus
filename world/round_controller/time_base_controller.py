import time

from world.round_controller.base_round_controller import BaseRoundController


class TimeBaseController(BaseRoundController):
    def wait(self):
        # 根据一个step在现实时间的映射，等待一段时间
        time.sleep(self.seconds_of_step)

    def __init__(self, steps_of_round, seconds_of_step):
        super().__init__(steps_of_round)
        self.seconds_of_step = seconds_of_step
