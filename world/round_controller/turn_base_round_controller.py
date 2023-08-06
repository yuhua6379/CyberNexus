from queue import Queue

from world.round_controller.base_round_controller import BaseRoundController


class TurnBaseController(BaseRoundController):
    def wait(self):
        # 等待指令，返回不重要，触发起来即可
        self.queue.get()

    def __init__(self, steps_of_round):
        super().__init__(steps_of_round)
        self.queue = Queue()

    def move_to_next_step(self):
        # 让控制器移动一步
        self.queue.put(1)
