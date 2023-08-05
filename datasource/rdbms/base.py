from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel


class RdbmsType(Enum):
    Sqlite = "sqlite"


class Rdbms(BaseModel):
    uri: str
    type: RdbmsType

    # 线程池的数量
    pool_size: int = 10


class RDBMSBase(ABC):

    def __init__(self, conf: Rdbms):
        self.conf = conf

    @abstractmethod
    def get_session(self):
        pass
