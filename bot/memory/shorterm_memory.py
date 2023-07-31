from abc import abstractmethod
from datetime import datetime
from typing import Dict, Any, List

from langchain.schema import BaseMemory
from pydantic import BaseModel

from datasource.rdbms.sqlite import get_session, HistoryModel, CharacterModel


class History(BaseModel, orm_mode=True):
    character1_id: int
    character2_id: int
    character1_name: str
    character2_name: str
    character1_message: str
    character2_message: str

    create_time: datetime

    @classmethod
    def build_short_term_memory(cls, history: HistoryModel):
        with get_session() as session:
            c1 = session.query(CharacterModel).get(history.character1_id)
            c2 = session.query(CharacterModel).get(history.character2_id)
            return cls(character1_id=history.character1_id,
                       character2_id=history.character2_id,
                       character1_name=c1.name,
                       character2_name=c2.name,
                       character1_message=history.character1_message,
                       character2_message=history.character2_message,
                       create_time=history.create_time
                       )

    def __str__(self):
        return (f"{self.character1_name}: {self.character1_message}\n"
                f"{self.character2_name}: {self.character2_message}")


class ShortTermMemory(BaseMemory):
    class BaseLimiter:
        @abstractmethod
        def limit(self, statement):
            pass

    class LengthLimiter(BaseLimiter):

        def __init__(self, cnt: int):
            self.cnt = cnt

        def limit(self, statement):
            return statement.limit(self.cnt).all()

    character1_id: int
    character2_id: int
    limiter: BaseLimiter

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        with get_session() as session:
            history = HistoryModel()
            history.character1_id = self.character1_id
            history.character2_id = self.character2_id
            history.character1_message = inputs["input"]
            history.character2_message = outputs["output"]
            session.add(history)
            session.commit()

    @property
    def memory_variables(self) -> List[str]:
        return ["history"]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve all messages from db"""
        with get_session() as session:
            statement = session.query(HistoryModel).filter(
                HistoryModel.character1_id == self.character1_id
                and HistoryModel.character2_id == self.character2_id
            )
            results = self.limiter.limit(statement)
            messages = []
            for record in results:
                message = History.build_short_term_memory(record)
                messages.append(message)
            return {"history": messages}

    def clear(self) -> None:
        pass
