from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel


class VectorDBType(Enum):
    Chromadb = "chromadb"


class VectorDB(BaseModel):
    uri: str
    type: VectorDBType


class VectorDbBase(ABC):

    def __init__(self, conf: VectorDB):
        self.conf = conf

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass
