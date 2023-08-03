from datetime import datetime

from pydantic import BaseModel

from datasource.rdbms.entities import HistoryModel
from repo.character import Character


class History(BaseModel, orm_mode=True):
    character1_id: int
    character2_id: int
    character1_name: str
    character2_name: str
    character1_message: str
    character2_message: str

    create_time: datetime

    @classmethod
    def from_orm(cls, history: HistoryModel):
        c1 = Character.get(history.character1_id)
        c2 = Character.get(history.character2_id)
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
