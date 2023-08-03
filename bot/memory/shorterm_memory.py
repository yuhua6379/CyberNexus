from abc import abstractmethod
from typing import Dict, Any, List

from langchain.schema import BaseMemory

from datasource.config import rdbms_instance
from datasource.rdbms.entities import HistoryModel
from repo.history import History


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
        with rdbms_instance.get_session() as session:
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
        with rdbms_instance.get_session() as session:
            statement = session.query(HistoryModel).filter(
                HistoryModel.character1_id == self.character1_id
                and HistoryModel.character2_id == self.character2_id
            )
            results = self.limiter.limit(statement)
            messages = []
            for record in results:
                record: HistoryModel
                message = History.from_orm(record)
                messages.append(message)
            return {"history": messages}

    def clear(self) -> None:
        pass
