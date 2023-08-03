from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel

from datasource.vectordb.entities import Document, Response


class VectorDBType(Enum):
    Chromadb = "chromadb"


class VectorDB(BaseModel):
    uri: str
    type: VectorDBType


class VectorDbBase(ABC):

    def __init__(self, conf: VectorDB):
        self.conf = conf

    @abstractmethod
    def batch_query(self, query_texts: List[str]) -> List[Tuple[str, List[Response]]]:
        pass

    def query(self, query_text) -> List[Response]:
        return self.batch_query([query_text])[0][1]


