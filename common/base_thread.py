import logging
import threading
from abc import abstractmethod
from typing import Callable

from common.log.logger import create_file_logger

_global_thread_dict = dict()
_global_logger_names = set()


def get_logger():
    global _global_thread_dict
    thread_id = threading.current_thread().ident
    logger = _global_thread_dict.get(thread_id)
    if logger is None:
        # 主线程用root写到console
        return logging.getLogger("root")
    else:
        return logger[0]


class BaseThread(Callable):

    def __init__(self, logger_name):
        global _global_logger_names

        if logger_name in _global_logger_names:
            raise RuntimeError(f"duplicate logger_name: {logger_name}")

        self.th = threading.Thread(target=self)
        _global_logger_names.add(logger_name)
        self.logger_name = logger_name

    @abstractmethod
    def run(self):
        pass

    def start(self):
        self.th.start()

    @property
    def log(self):
        return get_logger()

    def __call__(self, *args, **kwargs):
        self.local_data = threading.local()
        # 在线程被调起的时候创建一个特别的，独立的logger对象，服务整个线程
        # 主线程不会创建
        global _global_thread_dict
        thread_id = threading.current_thread().ident
        _global_thread_dict[thread_id] = (create_file_logger(self.logger_name), self.th)

        self.run()
